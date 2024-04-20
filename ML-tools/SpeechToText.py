import requests
import os

hugging_key = os.environ.get("HUGGING_KEY")
API_URL = "https://api-inference.huggingface.co/models/dima806/facial_emotions_image_detection"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {hugging_key}", 
    "Content-Type": "audio/flac"  
}