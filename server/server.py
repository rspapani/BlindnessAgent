from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os

from utils.ConvoCoach import ConvoCoach

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

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

    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        file.save("tempnew.webm")

        with open("tempnew.webm", "rb") as audio_file:
            audio_data = audio_file.read()

        print("success")
        # feedback = machine.add_clipd(audio_data, 0)
        # print(feedback)

        return jsonify({"message": "File successfully uploaded"}), 200
    
    return jsonify({"error": "File type not allowed"}), 400


@app.route('/dummy_endpoint', methods=['GET'])
def dummy_endpoint():
    return jsonify({'message': 'This is a dummy endpoint'}), 200

if __name__ == '__main__':
    app.run(debug=True)

