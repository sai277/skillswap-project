from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import CustomUser, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from session_requests.models import Badge, UserBadge, SessionRequest
from skills.models import UserSkills, LearnerProfile
from feedback.models import Feedback
from .utils import check_and_award_badges

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST.get('address', '')
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST.get('user_type')  # <-- NEW
        bio = ""  # Optional: leave blank initially

        email = email.lower()

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("signup")
        if CustomUser.objects.filter(contact_number=phone).exists():
            messages.error(request, "Phone number already exists!")
            return redirect("signup")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                contact_number=phone,
                profile_picture=profile_picture,
                password=password
            )
            UserProfile.objects.create(
                user=user,
                location=address,
                user_type=user_type,
                bio=bio,
                availability={}
            )
            messages.success(request, 'Account has been registered. Login now.')
            return redirect("login")
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect("signup")
    else:
        return render(request, "signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")  # use named URL if available

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Optional: update last_active
            user.last_active = datetime.now()
            user.save(update_fields=['last_active'])
            messages.success(request, "You are now logged in.")
            return redirect("index")  # Redirect to your index page
        else:
            messages.error(request, "Incorrect Username or Password!")
            return redirect("login")

    return render(request, "login.html")

@login_required(login_url="/login")
def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		messages.success(request,"You are logged out.")
		return redirect("login")
	else:
		messages.error(request,"You are not Logged in.")
		return redirect("login")

@login_required(login_url="/login")
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)

    check_and_award_badges(request.user)  # ← Badge evaluator here

    earned_badges = UserBadge.objects.filter(user=request.user).select_related('badge')

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile,
        'earned_badges': earned_badges,
    })

@login_required(login_url="/login")
def edit_profile_view(request):
    user = request.user
    profile = user.profile  # Assuming OneToOne relation

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '').lower()
        contact_number = request.POST.get('contact_number', '')
        location = request.POST.get('location', '')
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture')

        # Validation checks
        if CustomUser.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("edit_profile")

        if CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("edit_profile")

        if CustomUser.objects.exclude(pk=user.pk).filter(contact_number=contact_number).exists():
            messages.error(request, "Phone number already exists!")
            return redirect("edit_profile")

        # Update user info
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.contact_number = contact_number
        user.save()

        # Update profile info
        profile.location = location
        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, 'edit_profile.html', {
        'user': user
    })

def index(request):
    soft_skills = []
    technical_skills = []
    interests = []
    feedbacks = []
    sessions = []

    session_action = request.GET.get('session_action')  # 👈 get query param

    if request.user.is_authenticated:
        try:
            user_skills = UserSkills.objects.get(user=request.user)
            skills_data = user_skills.data or {}
            soft_skills = skills_data.get("softSkills", [])
            technical_skills = skills_data.get("technicalSkills", [])
        except UserSkills.DoesNotExist:
            pass

        try:
            learner_profile = LearnerProfile.objects.get(user=request.user)
            interests = learner_profile.interests or []
        except LearnerProfile.DoesNotExist:
            pass

        feedbacks = Feedback.objects.filter(user=request.user).order_by('-submitted_at')
        sessions = SessionRequest.objects.filter(learner=request.user).order_by('-date', '-time')

    context = {
        'soft_skills': soft_skills,
        'technical_skills': technical_skills,
        'interests': interests,
        'feedbacks': feedbacks,
        'sessions': sessions,
        'session_action': session_action,  # 👈 pass to template
    }
    return render(request, "index.html", context)


