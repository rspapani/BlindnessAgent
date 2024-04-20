from openai import OpenAI
import base64
import os

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_gpt4(image_path):
    client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))

    base64_image = encode_image_to_base64(image_path)
    image_data = f"data:image/jpeg;base64,{base64_image}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a highly capable AI trained to analyze images."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "What’s in this image?"
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

if __name__ == "__main__":
    print(analyze_image_with_gpt4('images/drinks.jpg'))
