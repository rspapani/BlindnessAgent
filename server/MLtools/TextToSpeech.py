#The name's Blind, James Blind 

from openai import OpenAI

import os

from dotenv import load_dotenv
load_dotenv()

    
def openai_tts(feedback, timestamp):
    print("Getting Audio Data")
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=feedback
    )

    try:
        response.stream_to_file(f"./feedback_audio/feedback_at_{timestamp}.mp3")
        return f"feedback_at_{timestamp}.mp3", 0
    except Exception as e:
        print(e)
        return "failed", 1

if __name__ == "__main__":
    print(openai_tts("Hey have you considered not doing this?", 0))