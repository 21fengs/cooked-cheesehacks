from flask import Flask, request, jsonify
import json
from flask_cors import CORS, cross_origin

from tools import create_midi_file
from model import run_model

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests

@app.route("/members")
def members():
    return {"members": ["Member1", "pls work", "im begging u"]}

@app.route("/music_sheet")
def music_sheet():
    return {"musicSheet": ["A", "B", "C"]}

# @app.route('/convert_to_midi', methods=['POST'])
# def convert_to_mid(FUNCTION=None): 
#     # TODO: fix the connection, so you take array, call convert to midi
#     exec(FUNCTION.replace("<br>", "\n"))    
#     return ""

# @app.route('/process-data', methods=['POST'])
# def process_data():
#     try:
#     # Ensure the data is valid JSON
#         music_sheet_data = request.json
#         if music_sheet_data is None:
#             raise ValueError("No JSON data received")
#         else: 
#             print(music_sheet_data)
#             some_python_function(notes=music_sheet_data, file="output.mid")
#     except Exception as e:
#         # Log the error and return a response
#         print("Error occurred:", str(e))

#     return {"musicSheet": ["wtf"]}


@app.route('/process_data', methods=["GET", "POST"])
def process_data():
    if request.method == "POST":
        print("POST RECEIVED!!!!!!")
        music_sheet_data = request.json        
        if music_sheet_data is None:
            raise ValueError("No JSON data received")
        else: 
            print(music_sheet_data)
            create_midi_file(notes=music_sheet_data, file="output.mid")
            # TODO: start model
            run_model()
        return jsonify({"status": "success!!!!"}), 200
        # I think you want to increment, that case ButtonPressed will be plus 1.
    else:
        return jsonify({"status": "empty"}), 200

    # try:
    #     data = request.json  # Get JSON data from the request
    #     print("Received data:", data)  # Log it to the console (or use it in your function)
        
    #     # Example of calling a function based on the data
    #     result = some_python_function(data)
        
    #     return jsonify({"status": "success", "result": result}), 200
    # except Exception as e:
    #     return jsonify({"status": "error", "message": str(e)}), 500

def some_python_function(data):
    # Example of a simple Python function that processes the data
    return f"Processed data: {data}"


def send_file_to_model(output_file):
    # TODO for shawwwn wooo
    return 0



# def process_data():
#     data = request.json  # Get JSON data from the request
#     print("Received data:", data)  # Call your function here if needed
#     # Example function call
#     result = {"status": "success", "message": "Data processed!"}
#     return jsonify(result)  # Send a response back to the client


if __name__ == "__main__":
    app.run(debug=True)