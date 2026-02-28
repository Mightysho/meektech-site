# from django.db import models

# # Create your models here.


# class Visitor(models.Model):
#     ip_address = models.GenericIPAddressField()
#     path = models.CharField(max_length=500)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     user_agent = models.TextField(blank=True)
#     latitude = models.FloatField(blank=True, null=True)
#     longitude = models.FloatField(blank=True, null=True)
#     visited_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.ip_address} - {self.path}"

from django.db import models

# Create your models here.


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=500)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path}"


