from HuggingWrapper import get_query

API_URL = "https://api-inference.huggingface.co/models/dima806/facial_emotions_image_detection"

fer_query = get_query(API_URL=API_URL)

if __name__ == "__main__":
    print(fer_query(filename="../refimages/happy.jpeg"))
    print(fer_query(filename="../refimages/sad.jpeg"))