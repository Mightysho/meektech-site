# ai.py
from openai import OpenAI
from meektech import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_ai_response(message):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        # messages=[
        #     {"role": "system", "content": "You are Meek Technology support assistant."},
        #     {"role": "user", "content": message}
        # ]
        messages=[
            {
                "role": "system",
                "content": """
                You are Meek Technology's support assistant.

                Services:
                - Software Development
                - Website Design
                - Mobile App Development
                - UI/UX Design
                - IT Consulting
                - AI Solutions

                If a user requests human support,
                tell them a support agent has been notified.
                """
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return response.choices[0].message.content


