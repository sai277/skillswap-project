from django.shortcuts import render, redirect, get_object_or_404
from .models import SessionRequest, UserBadge
from django.contrib.auth.decorators import login_required
from datetime import datetime
from feedback.models import Feedback
from django.contrib import messages
from django.urls import reverse

@login_required
def request_session(request, mentor_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    mentor = get_object_or_404(User, id=mentor_id)

    if request.method == "POST":
        scheduled_datetime = request.POST.get('scheduled_time')
        if scheduled_datetime:
            dt = datetime.fromisoformat(scheduled_datetime)
            date = dt.date()
            time = dt.time()
            message = request.POST.get('message', '')
            SessionRequest.objects.create(
                learner=request.user,
                mentor=mentor,
                date=date,
                time=time,
                message=message
            )
            return redirect('session_list')

    return render(request, 'request_session.html', {'mentor': mentor})

@login_required
def session_list(request):
    mentor_sessions = SessionRequest.objects.filter(mentor=request.user)
    learner_sessions = SessionRequest.objects.filter(learner=request.user)

    feedbacks = Feedback.objects.filter(user=request.user)
    submitted_feedback_sessions = feedbacks.values_list('session_id', flat=True)

    return render(request, 'session_list.html', {
        'mentor_sessions': mentor_sessions,
        'learner_sessions': learner_sessions,
        'submitted_feedback_sessions': submitted_feedback_sessions,
    })

@login_required
def respond_to_session(request, session_id, action):
    session = get_object_or_404(SessionRequest, id=session_id, mentor=request.user)
    if action in ['accept', 'reject']:
        session.status = 'accepted' if action == 'accept' else 'rejected'
        session.save()
    return redirect('session_list')

@login_required
def dashboard(request):
    # Fetch the user's sessions (both learner and mentor)
    learner_sessions = SessionRequest.objects.filter(learner=request.user)
    mentor_sessions = SessionRequest.objects.filter(mentor=request.user)

    # Fetch the user's badges
    user_badges = UserBadge.objects.filter(user=request.user)

    # Calculate the session status counts
    pending_sessions = learner_sessions.filter(status='pending').count() + mentor_sessions.filter(status='pending').count()
    accepted_sessions = learner_sessions.filter(status='accepted').count() + mentor_sessions.filter(status='accepted').count()
    rejected_sessions = learner_sessions.filter(status='rejected').count() + mentor_sessions.filter(status='rejected').count()

    context = {
        'learner_sessions': learner_sessions,
        'mentor_sessions': mentor_sessions,
        'user_badges': user_badges,
        'pending_sessions': pending_sessions,
        'accepted_sessions': accepted_sessions,
        'rejected_sessions': rejected_sessions
    }

    return render(request, 'dashboard.html', context)

def respond_to_session(request, session_id, action):
    session = get_object_or_404(SessionRequest, id=session_id)

    if action == 'accept':
        session.status = 'accepted'
        messages.success(request, "✅ Session accepted successfully.")
    elif action == 'reject':
        session.status = 'rejected'
        messages.warning(request, "❌ Session rejected.")

    session.save()
    # Redirect to dashboard with a session_action query param
    return redirect(f'{reverse("dashboard")}?session_action={action}')
