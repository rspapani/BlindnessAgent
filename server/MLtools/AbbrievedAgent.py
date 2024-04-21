#The name's Blind, James Blind 

from openai import OpenAI
import base64
import os

from dotenv import load_dotenv
load_dotenv()

    
def shortfeedback_with_gpt4(transcript, feedback):
    print("sending convo to gpt")
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, highly trained, AI speech coach whose job is to help neurodivergent individuals better understand social cues i.e. help them read the room, and provide live feedback mid conversation.  Specifically, you are called in to analyze live conversation transcripts as heard by your client and provide realtime feedback as to how well they are matching, and responding to the emotional response of the person speaking to them. Your task is to take existing feedback, contextualize it with the transcript provided, and distill it to a short sentence that can be provided to the speaker mid conversation without interrupting their train of thought or flow"
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""Here is some feedback from a similar speech coach to a conversation, this feedback will be available to the speaker at a later point, but I want you to shorten the feedback into a short sentence less than 15 words which can be provided to the speaker mid conversation.  An example could be "tone down the comments on xyz" or "stop with the jokes about xyz" or "rephrase how you said xyz" 
                
                here is the transcript: {transcript}
                here is the long feedback: {feedback}

                Try to make at least one specific reference to what was said"""
                }
            ]
            }
        ])

    return response.choices[0].message.content if response.choices else "No response."


