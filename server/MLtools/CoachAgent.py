#The name's Blind, James Blind 

from openai import OpenAI
import base64
import os

from dotenv import load_dotenv
load_dotenv()

    
def analyze_convo_with_gpt4(transcript, fer, ser1, ser2):
    print("sending convo to gpt")
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, highly trained, AI speech coach whose job is to help neurodivergent individuals better understand social cues i.e. help them read the room, and provide live feedback mid conversation.  Specifically, you are called in to analyze live conversation transcripts as heard by your client and provide realtime feedback as to how well they are matching, and responding to the emotional response of the person speaking to them.  Provided with every transcripts is a tonal analysis of both the client and their speech partnet, as well as a facial emotional analysis of their speech partner.  In your response you should take into consideration what their expession as well as tone may indicate with the context of what is being said and the tone of the clent."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""Mid conversation we have noticed that the expression of the person I am speaking to has changed drastically and I am not sure what to make of it.  I need you to provide feedback ONLY if I have said something egregious or otherwise commited a social faux pass without realizing it.  If it is a minor issue or otherwise not major and simply end your response with No Feedback.  
                
                Provided here is the facial emotion recognition of the person I am speaking with: {fer}
                
                Here is the emotional tone analysis of the other speaker {ser2}
                
                Here is the emotional tone analysis of me: {ser1}
                
                Here is a transcript of the last 30 seconds of conversation:
                {transcript}"""
                }
            ]
            }
        ])

    return response.choices[0].message.content if response.choices else "No response."


