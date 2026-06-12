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


def activate_human_support(request, session_id):

    session = ChatSession.objects.get(id=session_id)

    session.is_human_active = True
    session.assigned_agent = request.user
    session.save()

    return JsonResponse({
        "success": True
    })

