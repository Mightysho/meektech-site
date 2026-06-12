# ai.py
from openai import OpenAI
from meektech import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_ai_response(message):
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "You are Meek Technology support assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content


