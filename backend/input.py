import mido
from mido import MidiFile, MidiTrack, Message

"""
Creates a MIDI file from a list of notes.

Params:
    notes (list): A list of tuples:
        - Note (int): MIDI note number (e.g., 60 for middle C).
        - Duration (int): Duration of the note in ticks.
    output_filename (str): The name of the output MIDI file.
"""
def create_midi_file(notes, file="output.mid"):
    midi_mapping = {'A': 57, 
                'B_b/A_#': 58,
                'B': 59,  
                'C': 60,
                'C_#/D_b': 61,
                'D':62,
                'E_b/D_#': 63,
                'E': 64,
                'F':65,
                'F_#/G_b':66,
                'G':67,
                'G_#/A_b':68
    }
    print("notes")
    print(notes)

    # Create a new MIDI file and track
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    # # Add notes to the track
    # for note, duration in notes:
    #     # Start the note
    #     track.append(Message('note_on', note=note, velocity=64, time=0))
    #     # Stop the note after the duration
    #     track.append(Message('note_off', note=note, velocity=64, time=duration))
    # Add notes to the track
    for note in notes:
        # Start the note
        midi_note = midi_mapping[note]

        print(str(midi_note))
        track.append(Message('note_on', note=midi_note, velocity=64, time=0))
        # Stop the note after the duration
        track.append(Message('note_off', note=midi_note, velocity=64, time=480))

    # Save the MIDI file
    midi.save(file)
    print(f"MIDI file saved in {file}")

# Example usage
notes = [
    (60, 480),  # Middle C, duration 480 ticks
    (62, 480),  # D, duration 480 ticks
    (64, 480),  # E, duration 480 ticks
    (65, 480),  # F, duration 480 ticks
    (67, 480)   # G, duration 480 ticks
]

# create_midi_file(notes, "input_files/it-worked.mid")
