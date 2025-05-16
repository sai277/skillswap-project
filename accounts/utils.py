from django.utils.timezone import now, timedelta
from session_requests.models import SessionRequest
from feedback.models import Feedback
from .models import UserProfile  # adjust if needed
from session_requests.models import Badge, UserBadge

def check_and_award_badges(user):
    def award(badge_name):
        badge = Badge.objects.get(name=badge_name)
        UserBadge.objects.get_or_create(user=user, badge=badge)

    sessions = SessionRequest.objects.filter(learner=user)
    feedbacks = Feedback.objects.filter(user=user)

    # 1. Early Bird
    if sessions.filter(time__lt="08:00:00").exists():
        award("Early Bird")

    # 2. Active Learner
    if sessions.count() >= 5:
        award("Active Learner")

    # 3. Star Mentor (received 5 thumbs up)
    if Feedback.objects.filter(session__mentor=user, rating="up").count() >= 5:
        award("Star Mentor")

    # 4. Helpful Feedback (left comments)
    if feedbacks.exclude(comment__isnull=True).exclude(comment__exact="").exists():
        award("Helpful Feedback")

    # 5. Consistent Performer (sessions over 3 weeks)
    recent_sessions = sessions.order_by('date').values_list('date', flat=True)
    weeks = set(d.isocalendar()[1] for d in recent_sessions)
    if len(weeks) >= 3:
        award("Consistent Performer")

    # 6. Feedback Star (got feedback from 3 users)
    feedback_user_count = Feedback.objects.filter(session__mentor=user).values('user').distinct().count()
    if feedback_user_count >= 3:
        award("Feedback Star")

    # 7. Quick Responder (dummy logic here)
    # Add logic if you store response timestamps

    # 8. Reliable Mentor (assume all accepted sessions attended)
    mentor_sessions = SessionRequest.objects.filter(mentor=user, status='accepted')
    if mentor_sessions.exists() and mentor_sessions.count() == mentor_sessions.count():
        award("Reliable Mentor")

    # 9. Learning Streak (5 consecutive days)
    dates = sorted(set(s.date for s in sessions))
    streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            streak += 1
        else:
            streak = 1
        if streak >= 5:
            award("Learning Streak")
            break

    # 10. Motivator
    if Feedback.objects.filter(comment__icontains="good job", user=user).exists():
        award("Motivator")

    # 11. Milestone Reached
    if sessions.count() >= 10:
        award("Milestone Reached")

    # 12. Top Rated (assumes only 'up' = positive)
    total = Feedback.objects.filter(session__mentor=user).count()
    if total >= 5:
        up = Feedback.objects.filter(session__mentor=user, rating='up').count()
        if (up / total) >= 0.9:
            award("Top Rated")

    # # 13. Growth Mindset
    # profile = UserProfile.objects.get(user=user)
    # if profile.skills:  # Assuming skills is a field
    #     award("Growth Mindset")

    # 14. Collaboration Pro
    if SessionRequest.objects.filter(learner=user, status='accepted').count() >= 3 and \
       SessionRequest.objects.filter(mentor=user, status='accepted').count() >= 3:
        award("Collaboration Pro")

    # 15. First Feedback
    if feedbacks.count() == 1:
        award("First Feedback")
