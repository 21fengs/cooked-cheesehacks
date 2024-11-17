from flask import Flask, render_template
import requests
import json
from input import create_midi_file

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members": ["Member1", "pls work", "im begging u"]}

@app.route("/music_sheet")
def music_sheet():
    return {"musicSheet": ["A", "B", "C"]}

# @app.route('/convert', methods=['POST'])
# def convert_to_mid():
#     data = request.json  # Get the data sent from the client
#     arrays = data.get('arrays')  # Assuming you send the array as `arrays`
    
#     output_file = "output.mid"
#     create_midi_file(arrays, output_file)  # Ensure this function saves the .mid file

#     # Return the .mid file to the client
#     return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)