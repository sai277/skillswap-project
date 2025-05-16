from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from accounts.models import CustomUser  # Import CustomUser

@login_required
def chat_view(request, user_id):
    other_user = CustomUser.objects.get(id=user_id)  # Use CustomUser
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    # Decrypt messages
    for msg in messages:
        msg.decrypted = msg.get_decrypted_message()

    if request.method == "POST":
        content = request.POST.get("message")
        if content:
            msg = Message(sender=request.user, receiver=other_user)
            msg.save_encrypted_message(content)
            return redirect('chat_view', user_id=other_user.id)

    return render(request, 'chat.html', {
        'messages': messages,
        'other_user': other_user
    })
