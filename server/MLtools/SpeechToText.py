import requests
import os

hugging_key = os.environ.get("HUGGING_KEY")
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {hugging_key}", 
    "Content-Type": "audio/flac"  
}

def whisper_query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

if __name__ == "__main__":
    print(whisper_query("../refaudio/TEDtalk.flac"))