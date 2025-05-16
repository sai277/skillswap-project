# session_requests/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SessionRequest, Badge, UserBadge

@receiver(post_save, sender=SessionRequest)
def award_badge_on_first_session(sender, instance, **kwargs):
    try:
        print("🚨 Signal fired for SessionRequest")  # New Debug Print

        if instance.status == 'accepted':
            print("✅ Session status is accepted")  # New Debug Print
            learner = instance.learner
            print(f"👤 Learner username: {learner.username}")  # New Debug Print

            total_sessions = SessionRequest.objects.filter(learner=learner, status='accepted').count()
            print(f"📊 Total accepted sessions for {learner}: {total_sessions}")

            if total_sessions == 1:
                badge, created = Badge.objects.get_or_create(
                    name='First Session',
                    defaults={'description': 'Completed your first session!' }
                )
                UserBadge.objects.get_or_create(user=learner, badge=badge)
                print("🏅 First Session badge awarded!")
            else:
                print("ℹ️ Learner already has accepted sessions. No badge awarded.")
        else:
            print(f"⛔ Session status is {instance.status}, not accepted")
    except Exception as e:
        print(f"❌ Error in awarding badge: {e}")