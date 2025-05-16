from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """
    Extends Django's built-in User model.
    - Uses email for authentication instead of username.
    - Adds profile picture, contact number, and verification.
    """
    email = models.EmailField(unique=True)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{9,15}$', 'Enter a valid phone number.')],
        blank=True,
        null=True
    )
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['username']  # Needed for createsuperuser

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    User profile linked to CustomUser.
    Stores user bio, location (address), type, and availability.
    """
    USER_TYPE_CHOICES = [
        ('learner', 'Learner'),
        ('mentor', 'Mentor'),
        ('both', 'Both')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField("Address", max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='both')

    # Availability: e.g., {"Saturday": [{"start": "18:00", "end": "23:00"}]}
    availability = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    def formatted_availability(self):
        """
        Returns a readable version of availability:
        Example: "Saturday: 18:00 - 23:00; Sunday: 10:00 - 02:30"
        """
        try:
            formatted = []
            for day, slots in self.availability.items():
                times = [f"{slot['start']} - {slot['end']}" for slot in slots]
                formatted.append(f"{day}: {', '.join(times)}")
            return "; ".join(formatted)
        except Exception:
            return "Invalid availability format"
