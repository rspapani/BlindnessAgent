import requests
import os

from dotenv import load_dotenv
load_dotenv()

hugging_key = os.getenv("HUGGING_KEY")
API_URL = "https://api-inference.huggingface.co/models/dima806/facial_emotions_image_detection"
headers = {"Authorization": f"Bearer {hugging_key}"}

def fer_query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

if __name__ == "__main__":
    print(fer_query("../refimages/happy.jpeg"))
    print(fer_query("../refimages/sad.jpeg"))