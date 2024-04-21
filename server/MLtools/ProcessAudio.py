from SpeechSentiment import sentiment_analysis
from SpeechToText import speech_query


def analyse_clip(audio):
    transcript = speech_query(data=audio)
    sentiment = sentiment_analysis(audio)

    return (transcript, sentiment)

def process_convo(audio):
    pass
    