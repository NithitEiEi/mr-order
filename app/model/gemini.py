import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

async def classify_img (image: bytes, prompt: str):
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, image])
    
    return response.text