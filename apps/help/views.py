from django.shortcuts import render
from .models import Faq, ChatSession, ChatMessage
from django.http import JsonResponse
from .ai_chat import get_ai_response
# Create your views here.

def faqfooter(request):
    frequently = Faq.objects.all()
    return render(request, "help/faq.html", {"frequently": frequently})
    

def ourterms(request):
    return render(request, "help/our-terms.html")
    

def privacypolicy(request):
    return render(request, "help/privacy-policy.html")
    
    
def chat_page(request):

    session_id = request.session.get("chat_session_id")

    if not session_id:
        chat_session = ChatSession.objects.create(
            visitor_name="Guest"
        )

        request.session["chat_session_id"] = chat_session.id

    return render(request, "help/chat.html")


#Chat API Endpoint
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_message(request):

    if request.method == "POST":

        session_id = request.session.get("chat_session_id")

        chat_session = ChatSession.objects.get(
            id=session_id
        )

        user_msg = request.POST.get("message")

        ChatMessage.objects.create(
            session=chat_session,
            sender="user",
            message=user_msg
        )

        # HUMAN SUPPORT ACTIVE
        if chat_session.is_human_active:

            return JsonResponse({
                "reply": "A support agent has joined the conversation and will reply shortly.",
                "human": True
            })

        # AI RESPONSE
        ai_reply = get_ai_response(user_msg)

        ChatMessage.objects.create(
            session=chat_session,
            sender="ai",
            message=ai_reply
        )

        return JsonResponse({
            "reply": ai_reply,
            "human": False
        })


def activate_human_support(request, session_id):

    session = ChatSession.objects.get(id=session_id)

    session.is_human_active = True
    session.assigned_agent = request.user
    session.save()

    return JsonResponse({
        "success": True
    })


@csrf_exempt
def request_human_support(request):

    session_id = request.session.get(
        "chat_session_id"
    )

    session = ChatSession.objects.get(
        id=session_id
    )

    session.is_human_active = True
    session.save()

    return JsonResponse({
        "message": "Human support requested."
    })


from django.contrib.auth.decorators import login_required
from .models import ChatSession

@login_required
def support_dashboard(request):

    sessions = ChatSession.objects.all().order_by("-created_at")

    return render(
        request,
        "help/support-dashboard.html",
        {
            "sessions": sessions
        }
    )


@login_required
def support_chat(request, session_id):

    session = ChatSession.objects.get(
        id=session_id
    )

    messages = session.messages.all()

    return render(
        request,
        "help/support-chat.html",
        {
            "session": session,
            "messages": messages
        }
    )


@csrf_exempt
@login_required
def admin_send_message(
    request,
    session_id
):

    if request.method == "POST":

        session = ChatSession.objects.get(
            id=session_id
        )

        message = request.POST.get(
            "message"
        )

        ChatMessage.objects.create(
            session=session,
            sender="admin",
            message=message
        )

        return JsonResponse(
            {
                "success": True
            }
        )


