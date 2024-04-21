# Example filename: main.py
import os
import httpx
from dotenv import load_dotenv
import threading
import pyaudio
import subprocess
import shutil
import os
import glob
import time
import librosa
import numpy as np


from pydub import AudioSegment


endfile="MLtools/end.wav"

def delete_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' has been deleted.")
    else:
        print(f"The folder '{folder_path}' does not exist.")


# def play_raw_audio(raw_audio, sample_rate=44100, channels=1, format=pyaudio.paInt16):
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=format,
#                     channels=channels,
#                     rate=sample_rate,
#                     output=True)
#
#     chunk_size = 1024
#     data = raw_audio[:chunk_size]
#     while data:
#         stream.write(data)
#         data = raw_audio[chunk_size:]
#
#     stream.stop_stream()
#     stream.close()
#     p.terminate()


from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    PrerecordedOptions,
)

load_dotenv()

# URL for the realtime streaming audio you would like to transcribe
URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"
#os.putenv("DG_API_KEY","cc562f9c961ae2767a83dea3fc7c9f7a1c6c61a3")
#API_KEY = os.getenv("DG_API_KEY")
API_KEY="cc562f9c961ae2767a83dea3fc7c9f7a1c6c61a3"
#print(API_KEY)
output_folder = "extracted_audio"
firstbyte=bytearray()
allspeakers = set()
fulltranscript = []




def delete_and_recreate_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)
        #print(f"Folder '{folder_path}' has been deleted.")
    # Recreate the folder
    os.makedirs(folder_path)
    #print(f"Folder '{folder_path}' has been recreated.")
delete_and_recreate_folder(output_folder)


# def extract_audio_bytes(audio_bytes, start_time, end_time):
#     # Assume sample rate of 44100 Hz, mono channel, 16-bit sample width
#     sample_rate = 44100
#     channels = 1
#     sample_width = 2
#
#     # Calculate start and end positions in terms of bytes
#     start_pos = int(start_time * sample_rate * channels * sample_width)
#     end_pos = int(end_time * sample_rate * channels * sample_width)
#
#     # Extract the relevant segment of audio bytes
#     extracted_bytes = audio_bytes[start_pos:end_pos]
#
#     return extracted_bytes

# def save_audio_file(eaudio_bytes, start_time, end_time):
#     output_file = f"{output_folder}/audio_{start_time}-{end_time}.wav"
#     with open(output_file, "wb") as f:
#         f.write(eaudio_bytes)
#     #print(f"Saved audio segment as: {filename}")

def split_audio_segment(input_file, speaker,start_time, end_time,output_file=None):
    try:
        if output_file is None:
            output_file = f"{output_folder}/audio_{speaker}_{start_time}-{end_time}.wav"
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            "-y",
            output_file
        ]
        subprocess.run(cmd, check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except Exception as e:
        print(e)


# locfile='in.wav'

def makeuberfiles(speaker):
    files=glob.glob(f"{output_folder}/audio_{speaker}_*")
    combined = AudioSegment.silent(duration=0)
    # Loop through the list of file paths and concatenate them

    for file in files:
        # Load the audio file
        current_audio = AudioSegment.from_file(file)
        # Append the current audio to the combined audio
        combined += current_audio

    # Export the combined audio to a file
    combined.export(f"{output_folder}/TotalFileSpeaker_"+str(speaker)+".wav", format="wav")


def trimendaudiofile(output_file,input_file):
    try:
        endfilelength=0.8
        end_time=librosa.get_duration(path=input_file)

        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(0.0),
            "-to", str(end_time-endfilelength),
            "-y",
            "-c", "copy",
            output_file
        ]
        subprocess.run(cmd, check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except Exception as e:
        print(e)
def mergeaudiofiles(file1,file2):
    combined = AudioSegment.silent(duration=0)
    # Loop through the list of file paths and concatenate them

    for file in [file1,file2]:
        # Load the audio file
        current_audio = AudioSegment.from_file(file)
        # Append the current audio to the combined audio
        combined += current_audio

    # Export the combined audio to a file
    combined.export(f"temp.wav", format="wav")

def read_audio_with_pydub(file_path):
    """
    Read an audio file using PyDub and return its contents as bytes.
    :param file_path: Path to the audio file.
    """
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Export to bytes
    audio_bytes = bytes(audio.raw_data)
    return audio_bytes

def diarize(locfileraw):
    try:
        locfile = "diarizationer.wav"
        
        def convert_webm_to_wav(input_file, output_file):
            # Command to convert webm to wav using ffmpeg
            command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',"-y", output_file]
            # Execute the command
            subprocess.run(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        convert_webm_to_wav(locfileraw, locfile)

        # STEP 1: Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)
        audio_bytes = bytearray()
        ocount=[0]
        icount=[0]
        mergeaudiofiles(locfile, endfile)
        #-------------------


        #-------------------
        # STEP 2: Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.live.v("1")

        # STEP 3: Define the event handlers for the connection
        def on_message(self, result, **kwargs):

            sentence = result.channel.alternatives[0].transcript
            #print(sentence)
            #print(result.channel.alternatives[0].words[0].speaker)
            if len(sentence) == 0:
                return

            speaker = result.channel.alternatives[0].words[0].speaker
            #print(result.channel.alternatives[0].words)
            start=result.channel.alternatives[0].words[0].start
            end=result.channel.alternatives[0].words[-1].end

            #print(start," ", end)
            print(f"Person {speaker}: {sentence}")
            fulltranscript.append(f"Person {speaker}: {sentence}")
            # if speaker in convo.keys():
            #       convo[speaker].append([start,end])
            # else:
            #       convo[speaker]=[[start, end]]
            split_audio_segment("temp.wav",speaker, start, end)
            allspeakers.add(speaker)
            # save_audio_file(extract_audio_bytes(audio_bytes, start, end),start,end)
            #print(start, " ",end, len(audio_bytes))
            #clocknogood=end-0.1
            #split_audio_segment("output_audio.wav", start-clocknogood, clocknogood,"output_audio.wav")
            print(end)
            icount[0]=end
        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        # STEP 4: Register the event handlers
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        # STEP 5: Configure Deepgram options for live transcription
        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            diarize= True,
        )

        # STEP 6: Start the connection

        ocount[0] = librosa.get_duration(path=locfile)
        dg_connection.start(options)

        # STEP 7: Create a lock and a flag for thread synchronization
        lock_exit = threading.Lock()
        exit = False
        # STEP 8: Define a thread that streams the audio and sends it to Deepgram
        def iter_bytes(file_path="temp.wav", chunk_size=1024):
            """ Generator that yields chunks of bytes from the specified file. """
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break  # If the chunk is empty, end of file is reached
                    yield chunk

        # Usage example
        def myThread():
            for data in iter_bytes():
                audio_bytes.extend(data)
                with open("extracted_audio/output_audio.wav", 'wb') as f:
                    f.write(audio_bytes)
                #play_raw_audio(data)
                dg_connection.send(data)


        # def myThread():
        #     with httpx.stream("GET", URL) as r:
        #         for data in r.iter_bytes():
        #             lock_exit.acquire()
        #             if exit:
        #                 break
        #             lock_exit.release()
        #             if len(firstbyte)==0:
        #                 firstbyte.extend(data)
        #             audio_bytes.extend(data)
        #             with open("extracted_audio/output_audio.wav", 'wb') as f:
        #                 f.write(audio_bytes)
        #             #play_raw_audio(data)
        #             dg_connection.send(data)
        # # STEP 9: Start the thread
        # "ic2.sslstream.com/wgdj-am"
        #
        #
        myHttp = threading.Thread(target=myThread)
        myHttp.start()

        # STEP 10: Wait for user input to stop recording
        #input("Press Enter to stop recording...\n\n")
        # STEP 11: Set the exit flag to True to stop the thread
        while (ocount[0]-icount[0])>0.01:
            #print(ocount[0]," ",icount[0])
            time.sleep(0.1)
        lock_exit.acquire()
        exit = True
        lock_exit.release()


        # STEP 12: Wait for the thread to finish
        myHttp.join()


        # STEP 13: Close the connection to Deepgram
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

    def substring_up_to_terminator(input_string, terminator):
        """
        Returns a substring from the beginning of input_string up to the first occurrence
        of the terminator character.
        :param input_string: The string from which to extract the substring.
        :param terminator: The termination character.
        :return: The substring up to the terminator. If the terminator is not found, returns the entire string.
        """
        # Find the index of the terminator character
        pos = input_string.find(terminator)
        # If terminator is found, return the substring up to it
        if pos != -1:
            return input_string[:pos]
        # If terminator is not found, return the whole string
        return input_string

    fulltranscripttxt="\n".join(fulltranscript[0:-1])
    # with open("transcript.txt","w") as f:
        # f.write(fulltranscripttxt)

    for ispeaker in allspeakers:
        makeuberfiles(ispeaker)
    endperson=(substring_up_to_terminator(fulltranscript[-1],":").replace("Person ",""))
    trimendaudiofile(f"{output_folder}/TempTotalFileSpeaker_" + str(endperson)+".wav", f"{output_folder}/TotalFileSpeaker_" + str(endperson)+".wav")
    os.replace(f"{output_folder}/TempTotalFileSpeaker_" + str(endperson)+".wav", f"{output_folder}/TotalFileSpeaker_" + str(endperson)+".wav")

    return fulltranscript[0:-1]

if __name__ == "__main__":
    print(diarize("../tempnew.webm"))
