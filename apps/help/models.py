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
