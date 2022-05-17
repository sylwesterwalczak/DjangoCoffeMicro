from django.db import models

class Message(models.Model):
    purchase_id = models.PositiveIntegerField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
