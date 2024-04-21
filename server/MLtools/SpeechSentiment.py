from transformers import AutoModelForAudioClassification
import librosa, torch
import time

import os
import soundfile as sf
import numpy as np

mappings = {0: 'Angry', 1: 'Sad', 2: 'Happy', 3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Contempt', 7: 'Neutral'}

#load model
model = AutoModelForAudioClassification.from_pretrained("3loi/SER-Odyssey-Baseline-WavLM-Categorical-Attributes", trust_remote_code=True)

#get mean/std
mean = model.config.mean
std = model.config.std


def sentiment_analysis(data="", filename=""):
    if data:
        # audio_data, samplerate = sf.read(io.BytesIO(data))

        # desired_samplerate = model.config.sampling_rate

        # if samplerate != desired_samplerate:
        #     raw_wav = librosa.resample(audio_data, orig_sr=samplerate, target_sr=desired_samplerate)
        # else:
        #     raw_wav = audio_data

        #FML IT WORKS BETTER
        with open("./MLtools/temp_sentiment.mp3", "wb") as f:
            f.write(data)

        print(os.listdir("./MLtools/"))

        raw_wav, _ = librosa.load("./restarded.mp3", sr=model.config.sampling_rate)

    else:
        raw_wav, _ = librosa.load(filename, sr=model.config.sampling_rate)


    norm_wav = (raw_wav - mean) / (std+0.000001)
    mask = torch.ones(1, len(norm_wav))

    wavs = torch.tensor(norm_wav).unsqueeze(0)

    with torch.no_grad():
        pred = model(wavs, mask)

    probabilities = {sentiment:prob
                     for sentiment, prob in
                     zip(mappings.values(), torch.nn.functional.softmax(pred, dim=1)[0].tolist()) }
    
    return probabilities


if __name__ == "__main__":

    x = time.time()
    print(os.listdir())
    print(sentiment_analysis(filename="restarted.mp3"))
    print(time.time() - x)

