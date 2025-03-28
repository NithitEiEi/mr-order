import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from model.prompt import prompt

load_dotenv()

client = OpenAI(
    base_url= os.getenv("LLM_URL"),
    api_key= os.getenv("LLM_API_KEY")
)

async def classify_order (text: str, menus: list, order: dict):
    input = f"""
        message: {text}
        old order: {order}

        menus: {menus}
    """

    completion = await client.chat.completions.create(
        model="mradermacher/openthaigpt1.5-7b-instruct-i1-GGUF",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input}
        ],
        temperature=0.1
    )
    data = json.loads(completion.choices[0].message.content)
    return data