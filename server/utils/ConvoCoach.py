import base64

from MLtools.EmotionAPI import fer_query
from MLtools.SpeechSentiment import sentiment_analysis


from MLtools.SpeechToText import speech_query

# from MLtools.TextToSpeech import tts
# from MLtools.diarization import diarize_and_clip

from MLtools.CoachAgent import analyze_convo_with_gpt4




negative_expressions = ["fear", "angry"]
thres = 0.5

class ConvoCoach():

    def __init__(self, max_memory=20, picrate=30):
        self.max_mem=max_memory
        self.max_pics=max_memory*picrate

        self.clips = [0]*self.max_mem
        self.ci = 0

        self.pics = [0]*self.max_pics
        self.pi = 0

        self.awaiting_audio = 0
        self.feedback_queue = []

    def add_pic(self, b64_img, timestamp):
        self.pics[self.ci%self.max_pics] = b64_img
        self.ci += 1

        fer, qerr = fer_query(data=base64.b64decode(b64_img[21:]))

        if qerr:
            return f"API error{fer['error']}"

        negative_facial_score = sum((fer[emot] for emot in negative_expressions))

        if negative_facial_score > thres:
            aud_tuple  = self.clips[(self.pi - 1)%self.max_mem]
            if aud_tuple and timestamp - aud_tuple[1] < 40:
                self.coach(aud_tuple[0], fer)

            self.awaiting_audio = fer

        return ",".join([f'{emote}: {perc}' for emote, perc in fer.items()])
    
    def add_clip(self, audio, timestamp):
        self.clips[self.ci%self.max_mem] = (audio, timestamp)
        self.ci += 1

        if self.awaiting_audio:
            self.coach(audio, self.awaiting_audio)
            self.awaiting_audio = 0

        outs = []
        while self.feedback_queue:
            outs.append(id(self.feedback_queue.pop()))

        return outs
    
    def add_clipd(self, audio, timestamp):
        self.clips[self.ci%self.max_mem] = (audio, timestamp)
        self.ci += 1

        transcript, qerr = speech_query(data=audio)

        
        if qerr:
            return f"API error{transcript['error']}"
        
        print(transcript)
        
        sentiment = sentiment_analysis(data=audio)

        print(sentiment)

        return transcript
    
    def coach(self, audio, fer):

        # transcript, speakers_clips = diarize_and_clip(audio)

        # sentiment_0 = sentiment_analysis(speakers_clips[0])
        # sentiment_1 = sentiment_analysis(speakers_clips[1])

        transcript = speech_query(data=audio)
        sentiment = sentiment_analysis(data=audio)


        print(f'\n\n Transcript: {transcript} \n\n  Sentiment: {sentiment} \n\n')

        self.feedback_queue.append(
            analyze_convo_with_gpt4(transcript, fer, sentiment, sentiment)
        )







    
