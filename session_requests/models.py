from django.db import models
from django.conf import settings

class SessionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    learner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learner_sessions')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_sessions')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.learner} ➡️ {self.mentor} on {self.date} at {self.time}"

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=255, blank=True)  # store icon name or emoji
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

