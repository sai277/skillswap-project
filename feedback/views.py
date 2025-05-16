# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from session_requests.models import SessionRequest
from .models import Feedback

@login_required
def feedback_page(request, session_id):
    session = get_object_or_404(SessionRequest, id=session_id)

    # Ensure only mentor or learner can give feedback
    if request.user != session.mentor and request.user != session.learner:
        return redirect('dashboard')

    feedback_submitted = False
    existing_feedback = Feedback.objects.filter(session=session, user=request.user).first()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating:
            messages.error(request, "Please select a rating before submitting.")
        elif existing_feedback:
            messages.info(request, "You have already submitted feedback for this session.")
        else:
            Feedback.objects.create(
                session=session,
                user=request.user,
                rating=rating,
                comment=comment
            )
            feedback_submitted = True

    return render(request, 'feedback.html', {
        'session': session,
        'feedback_submitted': feedback_submitted,
        'existing_feedback': existing_feedback
    })
