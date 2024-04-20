from HuggingWrapper import get_query

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

headers = {
    "Content-Type": "audio/flac"  
}

speech_query = get_query(API_URL=API_URL, cust_headers=headers)

if __name__ == "__main__":
    print(speech_query(filename="../refaudio/Rantman.flac"))