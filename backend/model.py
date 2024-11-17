# all python imports needed
import numpy as np
import tensorflow as tf
from music21 import *
from fractions import Fraction
import glob

# constants
NUM_PIANO_KEYS = 88
A0_MIDI_OFFSET = 21

# read in the mappings used for the offset and duration one hot encoding
def run_model():
    offset_map = dict()
    with open("weights/single_piece/offset_map.txt") as f:
        for line in f:
            key, value = line.strip().split(":")
            try:
                offset_map[float(key)] = int(value)
            except:
                offset_map[Fraction(key)] = int(value)
    reverse_offset = {offset_map[k]:k for k in offset_map}
    duration_map = dict()
    with open("weights/single_piece/duration_map.txt") as f:
        for line in f:
            key, value = line.strip().split(":")
            try:
                duration_map[float(key)] = int(value)
            except:
                duration_map[Fraction(key)] = int(value)
    reverse_duration = {duration_map[k]:k for k in duration_map}

    notes = []
    offsets = []
    durations = []

    # change path to read in different midi files
    for file in glob.glob('output.mid', recursive=True):
        try:
            mid = converter.parse(file)
        except:
            print(file)
            continue
        notes_to_parse = None
        prev_offset = 0
        notes_to_parse = mid.flatten().notes
        
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                # One hot encoding of pitch by piano key
                arr = np.zeros(NUM_PIANO_KEYS)
                try:
                    arr[element.pitch.midi - A0_MIDI_OFFSET] = 1
                except IndexError:
                    # removes files that had note outside the range of a piano
                    os.remove(file)
                    break
            
                notes.append(arr)
                durations.append(element.quarterLength)
                offsets.append(round(float(element.offset - prev_offset), 3))
                prev_offset = element.offset
                
            elif isinstance(element, chord.Chord):
                # if an element is a chord, encode each note separately
                isFirstNote = True
                for n in element:
                    arr = np.zeros(NUM_PIANO_KEYS)
                    try:
                        arr[n.pitch.midi - A0_MIDI_OFFSET] = 1
                    except IndexError:
                        try:
                            os.remove(file)
                            break
                        except FileNotFoundError:
                            break
                        
                    notes.append(arr)
                    durations.append(n.quarterLength)
                    
                    # offset of first note is chord offset, offset of other notes is 0
                    if isFirstNote:
                        offsets.append(round(float(element.offset - prev_offset), 3))
                        prev_offset = element.offset
                        isFirstNote = False
                    else:
                        offsets.append(float(0))

    notes = np.asarray(notes)
    #len(notes)

    # encodes the durations
    temp = []
    size = len(duration_map)
    for duration in durations:
        arr = np.zeros(size)
        arr[duration_map[duration]] = 1
        temp.append(arr)
    durations = np.asarray(temp)

    #encodes the offsets
    temp = []
    size = len(offset_map)
    for offset in offsets:
        arr = np.zeros(size)
        try:
            arr[offset_map[offset]] = 1
        except IndexError:
            print(offset, offset_map[offset])
            print(arr[offset_map[offset]])
        temp.append(arr)
    offsets = np.asarray(temp)

    # combines the three vectors per note into a single one
    train_notes = np.concatenate([notes, durations, offsets], axis = 1)
    inputs = [train_notes[:50]]

    input_size = len(inputs)
    inputs = np.asarray(inputs)
    inputs.reshape(input_size, min(len(train_notes), 50), len(train_notes[0]))

    # creates the model
    input_shape = inputs[0].shape
    learning_rate = 0.005

    inp = tf.keras.Input(input_shape)
    lstm = tf.keras.layers.LSTM(512)(inp)
    drop = tf.keras.layers.Dropout(0.5)(lstm)
    dense = tf.keras.layers.Dense(256)(drop)
    out = {
        "pitch": tf.keras.layers.Dense(NUM_PIANO_KEYS, name = "pitch", activation = "softmax")(dense),
        "duration": tf.keras.layers.Dense(len(duration_map), name = "duration", activation = "softmax")(dense),
        "offset": tf.keras.layers.Dense(len(offset_map), name = "offset", activation = "softmax")(dense),
    }

    model = tf.keras.Model(inp, out)

    model.compile(
        loss = "categorical_crossentropy",
        loss_weights = {
            'pitch': 1.0,
            'step': 1.0,
            'duration':1.0,
        },
        optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate),
        metrics = ["accuracy", "accuracy", "accuracy"]
    )
    #model.summary()

    # loads weights from the model trained beforehand
    model.load_weights("./weights/single_piece/weights.weights.h5")

    # generates new notes by adding the newly generated note to the end of the seed notes
    num_notes = 100
    generated_notes = [{"pitch": inputs[0][i][:NUM_PIANO_KEYS],
                        "duration": inputs[0][i][NUM_PIANO_KEYS:NUM_PIANO_KEYS + len(duration_map)],
                        "offset": inputs[0][i][-len(offset_map):]} for i in range(len(inputs[0]))]
    seed_notes = inputs[0]
    for i in range(num_notes):
        new_note = model.predict(tf.expand_dims(seed_notes, 0))
        new_input = np.concatenate([new_note["pitch"], new_note["duration"], new_note["offset"]], axis = 1)
        generated_notes.append(new_note)
        seed_notes = np.delete(seed_notes, 0, axis = 0)
        seed_notes = np.append(seed_notes, new_input, axis = 0)

    # turns the generated notes into music21 notes
    chord_builder = []
    note_stream = []
    offset = 0
    temperature = 1.5
    for i in reversed(range(len(generated_notes))):
        g = generated_notes[i]
        probs = g["pitch"].reshape(-1)
        pitch_idx = np.random.choice(len(probs), p=probs**temperature/np.sum(probs**temperature))

        n = note.Note(pitch_idx + A0_MIDI_OFFSET)
        try:
            n.quarterLength = float(reverse_duration[np.argmax(g["duration"])])
        except:
            n.quarterLength = Fraction(reverse_duration[np.argmax(g["duration"])])
        # if offset is 0, stores it so that it can be added to a chord
        offset = reverse_offset[np.argmax(g["offset"])]
        if offset == 0:
            chord_builder.append(n)
        elif len(chord_builder) == 0:
            note_stream.append((n, offset))
        else:
            note_stream.append((chord.Chord(chord_builder), offset))
            chord_builder = []
    if len(chord_builder) == 1:
        note_stream.append((chord_builder[0], 0))
    elif len(chord_builder) > 1:
        note_stream.append((chord.Chord(chord_builder), 0))
    note_stream.reverse()

    s = stream.Stream()
    previous_offset = 0
    for n, off in note_stream:
        previous_offset += off
        s.insert(previous_offset, n)

    # writes the midi file of the output
    s.write("midi", "final_music.mid")
