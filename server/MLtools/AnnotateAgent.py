#The name's Blind, James Blind 

from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

    
def annotatewithgpt(transcript, feedback):
    print("sending convo to gpt")
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, highly trained, AI transcript modification tool.  Your job is to read real conversation transcripts and annotate the transcript with the conversat feedback provided.  You are assisting an AI conversation coach in annotating a transcript with feedback."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""Here is a transcript of a conversation between two people, in alternating lines.  Your job is to take the feedback provided and insert relevant feedback lines between conversation.  I.e. if the feedback has to do with something said on line 5.  Create a new line immediately after that, assign the speaker as 'Speech Coach'.Lastly at the very end, add one final line from the speech coach giving a reccomendation on how the interaction could have gone better.  In the process try to fix any minor grammatical errors in the transcript, but only the grammer, keep the content as is. i.e. an output could be:

                Speaker 0: Hello Jerk
                Speech Coach: don't say jerk this may offend them
                Speaker 1: That makes me sad.
                Speech Coach: Next time don't insult the other person,try to complement them

                Here is the feedback: {feedback}
                Here is the transcript: {transcript}"""

                }
            ]
            }
        ])

    return response.choices[0].message.content if response.choices else "No response."


if __name__=="__main__":
    inpt = '\n'.join(['Person 0: How are you doing today?', "Person 0: I'm doing alright. How are you doing? Oh, I'm doing great. Isn't it a great day to", 'Person 1: That sounds like a nice thing to do.', "Person 0: You are a Jets fan. Right? I hate you. I hope you are hurt by Mike's comments.", 'Person 1: I would like to deny the allegations that I have', 'Person 1: jet fan. Okay. What sports team do you like?', 'Person 1: I I am not an avid watcher of Solitude.', "Person 1: So People who don't watch sports are even worse than jet fan.", "Person 0: Are terrible, and I don't need to die.", 'Person 1: I I So Noah, our sports are in lane.', 'Person 1: I am sad now because you', 'Person 1: said that. I hope that you die. Goodbye.'])

    fdbk = """The person you are speaking to is displaying a high level of sadness (70.07%) as indicated by the facial emotion recognition analysis. This high sadness score coincides with your conversation where the tone became negative and personal attacks were made, such as suggesting the other person is "terrible" and hoping they "die." These are strong and very inappropriate remarks that could deeply hurt someone\'s feelings and are likely the reason for the observed sadness.\n\nThis conversation has moved beyond typical jesting or light-hearted banter into more harmful territory, particularly with the death wishes. This constitutes a significant social misstep since it directly violates common social norms regarding respect and kindness in dialogue. The outcome is especially egregious in a casual social setting where such extreme language is unexpected and unwarranted.\n\nIt is important to recognize that even if such comments were meant humorously, they were not received as such, evidenced by the dominant emotion of sadness. It is advisable to apologize for the remarks that escalated the situation and to clarify intentions if they were misunderstood. Moving forward, it would be beneficial to keep the conversation topics lighter and to steer clear of personal jibes that could be interpreted as serious insults. \n\n**Feedback**: Apologize and attempt to mend the conversation by shifting to more neutral or positive topics. Make sure to maintain sensitivity to the other person\'s emotional responses to prevent further discomfort."""

    print(annotatewithgpt(inpt, fdbk))