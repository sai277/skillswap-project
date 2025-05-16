from django.db import models
from django.conf import settings
from session_requests.models import SessionRequest  # import your existing model

class Feedback(models.Model):
    RATING_CHOICES = [
        ('up', 'Thumbs Up'),
        ('down', 'Thumbs Down'),
    ]

    session = models.ForeignKey(SessionRequest, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, null=True)
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for session {self.session.id}"
