from flask import Flask, request, jsonify
from flask import send_from_directory, abort
import time

from flask_cors import CORS
import re
import os

from utils.ConvoCoach import ConvoCoach

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

FILE_DIRECTORY="./feedback_audio"

machine = ConvoCoach()   


image_encodings = []
@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image_base64' in data:
        image_base64 = data['image_base64']
        timestamp = int(data['timestamp'])

        fers = machine.add_pic(image_base64, timestamp)
        print(f'\n\n fer: {fers} \n\n')
        return jsonify({'message': f'Image analyzed {fers}'}), 200


    else:
        return jsonify({'error': 'No image_base64 field in the request body'}), 400

        
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    print("WE JUST GOT SOMETHING")
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        print("It's the real DEAL!")
        fname = f"temp_{time.time()}.webm"
        file.save(fname)

        with open(fname, "rb") as audio_file:
            audio_data = audio_file.read()

        deedback = machine.add_clip(audio_data, 0, fname)

        print(deedback)

        return jsonify({"feedback_path": deedback}), 200
        # return send_from_directory(FILE_DIRECTORY, deedback, as_attachment=True)
    
    return jsonify({"error": "File type not allowed"}), 400


@app.route('/dummy_endpoint', methods=['GET'])
def dummy_endpoint():
    return jsonify({'message': 'This is a dummy endpoint'}), 200

@app.route('/get_highlights', methods=['GET'])
def get_data():
    # with open("tempnew.webm", "rb") as audio_file:
    #     audio_data = audio_file.read()

    # deedback = machine.add_clip(audio_data, 0, "tempnew.webm")
    # print(deedback)
    # deedback = machine.add_clip(audio_data, 2, "temp.webm")
    # print(deedback)
    # print(machine.get_highlights())

    return jsonify(machine.get_highlights())

@app.route('/audio_feedback/<filename>')
def read_file(filename):
    # Ensure the filename does not contain any directory traversal characters
    if '..' in filename or filename.startswith('/'):
        return abort(400, description="Invalid filename.")

    # Construct the full path to the file
    filepath = os.path.join(FILE_DIRECTORY, filename)

    # Check if the file exists
    if not os.path.isfile(filepath):
        return abort(404, description="File not found.")

    # Serve the file
    return send_from_directory(FILE_DIRECTORY, filename, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)

