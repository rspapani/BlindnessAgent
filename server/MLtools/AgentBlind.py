#The name's Blind, James Blind 

from openai import OpenAI
import base64
import os

from dotenv import load_dotenv
load_dotenv()


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def analyze_b64img_with_gpt4(base64_image):
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    image_data = f"data:image/jpeg;base64,{base64_image}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, highly trained, AI vision assistant tasked with aiding those with vision impairments by describing their environment and answering any questions that they may have about it."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Please tell me what I am looking at, provided here is an image of what is directly in front of me"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": image_data
                }
                }
            ]
            }
        ])

    return response.choices[0].message.content if response.choices else "No response."

def analyze_image_with_gpt4(image_path):
    return analyze_b64img_with_gpt4(encode_image_to_base64(image_path))

if __name__ == "__main__":
    print(analyze_image_with_gpt4('../refimages/drinks.jpg'))
