import requests
import os

from dotenv import load_dotenv
load_dotenv()

hugging_key = os.getenv("HUGGING_KEY")
# API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

def_headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {hugging_key}"
}

def get_query(API_URL, cust_headers={}, transform=lambda x: x):
    headers = def_headers | cust_headers

    def query(data = "", filename = ""):
        if not data:
            with open(filename, "rb") as f:
                data = f.read()

        response = requests.post(API_URL, headers=headers, data=data)
        return transform(response.json())
    
    return query
