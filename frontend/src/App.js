import React, {useState, useEffect} from 'react'
import axios from 'axios'

const VALID_NOTES = [
  'A',
  'B_b/A_#',
  'B',
  'C',
  'C_#/D_b',
  'E_b/D_#',
  'E',
  'F',
  'F_#/G_b',
  'G',
  'G_#/A_b'
]

// const TEMPOS = [20, 40, 60, 100, 150, 200]

function ExecPythonCommand(pythonCommand) {
  var request = new XMLHttpRequest()
  request.open("GET", "/" + pythonCommand, true)
  request.send()
}

function testPrint() {
  const data = {};
  fetch('call_function', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data =>  {
    console.log('SUCCESS!!!: ', data.result);
  })
  .catch((error) => {
    console.error('Error:', error);
  })
  console.log("testprint working")
}

function App() {
  const [response, setResponse] = useState("");

  // TODO: setDuration lmao if everything else works
  const [inputMusic, setInputMusic] = useState([]);
  const addToMusic = (note) => {
    setInputMusic((music) => {
      return [...music, note]      
    })
  }  
  const resetMusic = () => {
    setInputMusic([]); // Resets inputMusic to empty array
  };
  // logs after each update to inputMusic
  useEffect(() => { 
    console.log(inputMusic)
  }, [inputMusic])

  // handles array->midi file button
  const midiClick = async () => {
    // const dataToSend = [(60, 480), (62, 480), (64, 480), (65, 480), (67, 480)];

    console.log("midi button clicked")
    
    try {
      const res = await axios.post('http://127.0.0.1:5000/process_data', inputMusic, {
        headers: {
          'Content-Type': 'application/json',  // Ensure it's JSON
        }
      });
      setResponse(res.data.result);  // Store server response
      console.log("Server Response:", res.data);
    } catch (error) {
      console.error("Error sending data:", error.response?.data || error.message);
      setResponse("Error: " + error.message);
    }
  };
  
  const [count, setCount] = useState(0)
  const [tempo, setString] = useState('')
  const [temp, setData] = useState([{}])

  // receive info from backend via json
  useEffect(() => { 
    fetch("/members").then(
      res => res.json()
    ).then( // puts backend json into var data
      temp => {
        setData(temp)
        console.log(temp)
      }
    )
  }, [])

  return (
    <div>
      <button type="button" onClick={midiClick}>
        Convert to MIDI Files
      </button>
      {/* <p>Response from server: {response}</p> */}
      {/* <button onClick={testPrint}>
        print testing button
      </button> */}
      <div className="Tempo">
        {/* <label>Song Tempo</label> // TODO: FIX LATER if have time
        <select onChange={(e) => {
          console.log(e.target.value)
        }}>
          {TEMPOS ? TEMPOS.map((TEMPOS) => {
          })}
          <option value="">Select</option>
        </select> */}
      </div>
      <br />
      <div className="row">
        <div className="col1-7">
          <h2>Notes, Click to add to input sheet music</h2>
          <u1 className="note-list">
            {
              VALID_NOTES.map((note) => {
                return <li key={note} className="note-list-item">
                  {note + " "} 
                  <button onClick={() => addToMusic(note)}>
                    Add
                  </button>
                </li>
              })
            }
          </u1>
          <h2>Sheet Music to be sent to the model</h2>
          <p>Sequence: {inputMusic.join(', \t')}</p>
          <button onClick={resetMusic}>Clear Sheet</button> 
        </div>
      </div>
    </div>
  )
}

export default App