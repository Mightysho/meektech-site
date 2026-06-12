from django.urls import path
from . import views

urlpatterns = [
    path("faq/", views.faqfooter, name="faq"),
    path("ourterms/", views.ourterms, name="our-terms"),
    path("privacypolicy/", views.privacypolicy, name="privacy-policy"),
    path("chat/", views.chat_page, name="chat"),
    path("send-message/", views.send_message, name="send_message"),
    path("activate-human/<int:session_id>/", views.activate_human_support, name="activate_human_support"),
    path("request-human/", views.request_human_support, name="request_human_support"),
    path("support-dashboard/", views.support_dashboard, name="support_dashboard"),
    path("support-chat/<int:session_id>/", views.support_chat, name="support_chat"),
    path("admin-send-message/<int:session_id>/", views.admin_send_message, name="admin_send_message"),
]


