import React, {useState, useEffect} from 'react'
// import create_midi_file from './/utils/input.py'

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

const button = document.getElementById('sendButton');

// button.addEventListener('click', () => {
//   fetch('/call_python_function', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     // You can send data to the Python function here if needed
//     // body: JSON.stringify({data: 'someData'})
//   })
//   .then(response => response.json())
//   .then(data => {
//     console.log(data.result); // Handle the result from Python
//   });
// });

// const TEMPOS = [20, 40, 60, 100, 150, 200]

function App() {
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
      {/* <div className="membersDisplay">
        {(typeof temp.members === 'undefined') ? (
            <p>Loading...</p>
        ) : (
          temp.members.map((member, i) => (
            <p key={i}>{member}</p>
          ))
        )} 
      </div> */}
      <div className="Tempo">
        {/* <label>Song Tempo</label> // TODO: FIX LATER F
        <select onChange={(e) => {
          console.log(e.target.value)
        }}>
          {TEMPOS ? TEMPOS.map((TEMPOS) => {

          })}
          <option value="">Select</option>
        </select> */}
      </div>
      <br />
      {/* <button onClick={() => setCount(count + 1)}>Press me +1</button> */}
      {/* <p>{count}</p> */}
      <button onClick={() => setString(tempo)}>Song Tempo</button>

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

      <br />
      <div>
        {/* <button onClick={create_midi_file()}>Send to Model to complete song</button>  */}

      </div>

    </div>
  )
}

export default App