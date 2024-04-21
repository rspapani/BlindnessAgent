import base64
import time

from MLtools.EmotionAPI import fer_query
# from MLtools.SpeechSentiment import sentiment_analysis


from MLtools.SpeechToText import speech_query

# from MLtools.TextToSpeech import tts
# from MLtools.diarization import diarize_and_clip

from MLtools.CoachAgent import analyze_convo_with_gpt4
from MLtools.AbbrievedAgent import shortfeedback_with_gpt4
from MLtools.TextToSpeech import openai_tts

from MLtools.diarator import diarize
from MLtools.AnnotateAgent import annotatewithgpt



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

        self.awaiting_audio = 0 #{'sad': 0.7006961703300476, 'fear': 0.13252848386764526, 'angry': 0.059667401015758514, 'happy': 0.04419358819723129, 'neutral': 0.04110799729824066}
        self.feedback_queue = []
        self.feedlog = {}

    def get_highlights(self):
        inorderlog = sorted(self.feedlog.items())
        print(inorderlog)

        outs = {}

        for i, log in enumerate(inorderlog):
            outs[f"Button {i + 1}: "] = log[1][-2]

        return outs



    def add_pic(self, b64_img, timestamp):
        self.pics[self.ci%self.max_pics] = b64_img
        self.ci += 1

        fer, qerr = fer_query(data=base64.b64decode(b64_img[21:]))

        if qerr:
            return f"API error{fer['error']}"

        negative_facial_score = sum((fer[emot] for emot in negative_expressions 
                                     if emot in fer))

        if negative_facial_score > thres:
            aud_tuple  = self.clips[(self.pi - 1)%self.max_mem]
            if aud_tuple and timestamp - aud_tuple[1] < 40:
                self.coach(aud_tuple[0], fer, aud_tuple[2])

            self.awaiting_audio = fer

        return ",".join([f'{emote}: {perc}' for emote, perc in fer.items()])
    
    def add_clip(self, audio, timestamp, filepath):
        self.clips[self.ci%self.max_mem] = (audio, timestamp, filepath)
        self.ci += 1

        if self.awaiting_audio:
            self.coach(audio, self.awaiting_audio, filepath, timestamp)
            # self.awaiting_audio = 0

        outs = []
        while self.feedback_queue:
            x = self.feedback_queue.pop()

            self.feedlog[x[0]] = x[1:]
            outs.append(x[-1])

        return outs
    
    def add_clipd(self, audio):
        # self.clips[self.ci%self.max_mem] = (audio, timestamp)
        # self.ci += 1

        transcript, qerr = speech_query(data=audio)

        
        if qerr:
            return f"API error{transcript['error']}"
        
        print(f'\n\n Transcript: {transcript}  \n\n')

        return analyze_convo_with_gpt4(transcript, 
                                       {'sad': 0.7006961703300476, 'fear': 0.13252848386764526, 'angry': 0.059667401015758514, 'happy': 0.04419358819723129, 'neutral': 0.04110799729824066})
    
    def coach(self, audio, fer, filepath, timestamp=0):

        timestamp = timestamp if timestamp else time.time()

        # transcript, speakers_clips = diarize_and_clip(audio)

        # sentiment_0 = sentiment_analysis(speakers_clips[0])
        # sentiment_1 = sentiment_analysis(speakers_clips[1])

        # transcript = speech_query(data=audio)
        # sentiment = sentiment_analysis(data=audio)

        transcript, qerr = speech_query(data=audio)

        
        if qerr or not 'transcript' in transcript:
            return f"API error{transcript['error']}"

        transcript = transcript['transcript']
        print(f'\n\n Transcript: {transcript}  \n\n')

        feedback = analyze_convo_with_gpt4(transcript, fer)
        short = shortfeedback_with_gpt4(transcript, feedback)

        if not ("NO FEEDBACK" in feedback or "NO FEEDBACK" in short):

            print(f'\n\n Feedback: {feedback}  \n\n')

            aud_path, _ = openai_tts(short, timestamp)

            diarized = diarize(filepath)
            print(diarized)

            if diarized:
                rdiz = self.clean_anno(diarized, feedback)
                sdiarized = [x.split(': ') for x in rdiz]

            else:
                print("DIARIZATION FAILURE")
                sdiarized = []

            print(f'\n\n Short: {short}  \n\n')

            self.feedback_queue.append((timestamp, short, feedback, sdiarized, aud_path))

            print(f'\n\n AudPath: {aud_path}  \n\n')

            print("COACHING ACCOMPLISHED")
        
        print("NO FEEDBACK")

    def clean_anno(self, diarized, feedback):
        raws = annotatewithgpt("\n".join(diarized), feedback)
        scr = lambda x: any([y in x for y in ['Person 0: ', 'Person 1: ', 'Speech Coach:']])
        return list(filter(scr, raws.split('\n')))



