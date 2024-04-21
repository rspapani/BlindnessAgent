from flask import Flask, request, jsonify
from flask_cors import CORS
import re

from utils.ConvoCoach import ConvoCoach

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

machine = ConvoCoach()

@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image_base64' in data:
        image_base64 = data['image_base64']
        timestamp = int(data['timestamp'])
        # image_base64 = re.search(r'base64,(.*)', image_base64).group(1)
        # image_encodings.append(image_base64)
        # print(timestamp)
        # return jsonify({'message': 'Image uploaded successfully'}), 200

        fers = machine.add_pic(image_base64, timestamp)
        print(f'\n\n fer: {fers} \n\n')
        return jsonify({'message': f'Image analyzed {fers}'}), 200

    else:
        return jsonify({'error': 'No image_base64 field in the request body'}), 400

        
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    data = request.get_json()
    if 'audio_url' in data:
        audio_url = data['audio_url']
        print(audio_url)
        timestamp = int(data['timetamp'])9
        # Assuming the data format is a URL pointing to the audio file
        # You might want to perform additional validation on the URL
        # return jsonify({'audio_link': audio_url}), 200

        feedback = machine.add_pic(audio_url, timestamp)
        print(f'\n\n fer: {feedback} \n\n')
        return jsonify({'message': f'Audio analyzed {feedback}'}), 200
    else:
        return jsonify({'error': 'No audio_url field in the request body'}), 400
    

@app.route('/dummy_endpoint', methods=['GET'])
def dummy_endpoint():
    return jsonify({'message': 'This is a dummy endpoint'}), 200

if __name__ == '__main__':
    app.run(debug=True)

