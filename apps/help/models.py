from django.db import models

# Create your models here.


class Faq(models.Model):
    Question = models.CharField(max_length=100, blank=True, null=True)
    Answer = models.TextField(blank=True, null=True)


    class Meta:
        # ordering = ["-created_at"]
        verbose_name_plural = "Frequently Asked Question"


    def __str__(self):
        return f"{self.Question}"


# class ChatMessage(models.Model):
#     user_id = models.CharField(max_length=100)
#     sender = models.CharField(max_length=20)  # 'user', 'ai', 'admin'
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     session_active = models.BooleanField(default=True)

#chat session

class ChatSession(models.Model):

    visitor_name = models.CharField(max_length=100)
    visitor_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_human_active = models.BooleanField(default=False)

    assigned_agent = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Chat #{self.id}"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"