import os
import json

import google.generativeai as genai
from PIL import Image

# Get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}/config.json"
config_data = json.load(open(config_file_path))

# Load the API key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# Configure google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)

#load model for chatbot
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

#function for image captioning
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    
    result = response.text
    return result


# image = Image.open("wallpaperflare.com_wallpaper (13).jpg")

# prompt = "tell me about this image"

# output = gemini_pro_vision_response(prompt, image)

# print(output)

def embedding_model_response(input_text):
    embedding_model = "model/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list

def gemini_pro_response(input_promt):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_vision_model.generate_content(input_promt)
    
    result = response.text
    return result