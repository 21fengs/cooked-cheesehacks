// MidiPlayerComponent.jsx
import React, { useEffect, useRef, useState } from 'react';
import './App.css'; // Import your CSS file

function MidiPlayerComponent() {
  const midiPlayerRef = useRef(null);
  const [midiSrc, setMidiSrc] = useState('');

  useEffect(() => {
    // Define custom elements to prevent React warnings
    if (typeof window !== 'undefined' && window.customElements) {
      class MidiPlayer extends HTMLElement {}
      class MidiVisualizer extends HTMLElement {}

      if (!customElements.get('midi-player')) {
        customElements.define('midi-player', MidiPlayer);
      }
      if (!customElements.get('midi-visualizer')) {
        customElements.define('midi-visualizer', MidiVisualizer);
      }
    }

    // Set attributes that React might not handle properly
    if (midiPlayerRef.current) {
      midiPlayerRef.current.setAttribute('sound-font', '');
    }
  }, []);

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setMidiSrc(e.target.result);
      };
      reader.readAsDataURL(file);
    } else {
      alert('Please select a valid MIDI file.');
    }
  };

  return (
    <div className="container">
      {/* File input for user to select MIDI file */}
      <input
        type="file"
        accept=".mid,audio/midi"
        onChange={handleFileChange}
        className="file-input"
      />

      {/* Only render the player if a MIDI source is available */}
      {midiSrc && (
        <>
          <midi-player
            ref={midiPlayerRef}
            src={midiSrc}
            visualizer="#myVisualizer"
          ></midi-player>
          <midi-visualizer
            type="piano-roll"
            id="myVisualizer"
          ></midi-visualizer>
        </>
      )}
    </div>
  );
}

export default MidiPlayerComponent;


