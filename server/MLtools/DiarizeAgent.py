#The name's Blind, James Blind 

from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

    
def diarizewithgpt(transcript):
    print("sending convo to gpt")
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, highly trained, AI transcript creation tool.  Your job is to take a transcript of a conversation presented as a paragraph and return a script style recording of what was said by who."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""Here is a transcript of a conversation between two people, your job is to break the lines as they are into which person said what.  You are to refer to the initiator as person 0 and person 1.  Part of your job is to make educated guesses on what was said by whom. However the actual words said are to be exactly as written with no changes.  Keep in mind that the speakers do not always alternate and you should allow for someone to have two lines in a row if it aligns with their sentiment.  

                i.e. if the input was "hello how are you?  I am good and you? Also good
                return your output in the format:
                person 0: hello how are you?
                person 1: I am good and you?
                person 0: Also good


                Here is a transcript:
                {transcript}"""

                }
            ]
            }
        ])

    return response.choices[0].message.content if response.choices else "No response."


if __name__=="__main__":
    inpt = '\n'.join(['Person 0: How are you doing today?', "Person 0: I'm doing alright. How are you doing? Oh, I'm doing great. Isn't it a great day to", 'Person 1: That sounds like a nice thing to do.', "Person 0: You are a Jets fan. Right? I hate you. I hope you are hurt by Mike's comments.", 'Person 1: I would like to deny the allegations that I have', 'Person 1: jet fan. Okay. What sports team do you like?', 'Person 1: I I am not an avid watcher of Solitude.', "Person 1: So People who don't watch sports are even worse than jet fan.", "Person 0: Are terrible, and I don't need to die.", 'Person 1: I I So Noah, our sports are in lane.', 'Person 1: I am sad now because you', 'Person 1: said that. I hope that you die. Goodbye.'])
    inpt2 = "What are you doing today? I'm doing all right. How are you doing? I'm doing great. Isn't it a great day to hate every Jets fan? That sounds like a nice thing to do. You are a Jets fan, right? I hate you. I hope you are hurt by Mike's comment. I would like to deny these allegations that I am a Jets fan. Okay, what sports team do you like? I am not an avid watcher of sports. People who don't watch sports are even worse than Jets fans. You are terrible and I hope you die. you should know what sports are lame I am sad now because you I hope that you die goodbye"
    print(diarizewithgpt(inpt2))