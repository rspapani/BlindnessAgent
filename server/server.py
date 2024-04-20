from flask import Flask, request, jsonify
from flask_cors import CORS
import re

from MLtools.AgentBlind import analyze_b64img_with_gpt4


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

image_encodings = []

@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image_base64' in data:
        image_base64 = data['image_base64']
        image_base64 = re.search(r'base64,(.*)', image_base64).group(1)
        image_encodings.append(image_base64)
        print(image_encodings)

        analysis = analyze_b64img_with_gpt4(image_base64)

        return jsonify({'message': analysis}), 200
    else:
        return jsonify({'error': 'No image_base64 field in the request body'}), 400

@app.route('/dummy_endpoint', methods=['GET'])
def dummy_endpoint():
    return jsonify({'message': 'This is a dummy endpoint'}), 200

if __name__ == '__main__':
    app.run(debug=True)
