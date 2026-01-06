from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, SessionRequest
from skills.models import Skill
from django.contrib.auth import get_user_model
from django.contrib import messages as django_messages

User = get_user_model()

@login_required
def chat_list(request):
    # Get all users the current user has messaged or received messages from
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=user_ids)
    
    return render(request, 'bookings/chat_list.html', {'chat_users': chat_users})

@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
        return redirect('chat_detail', user_id=user_id)
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'bookings/chat_detail.html', {
        'other_user': other_user,
        'messages': messages
    })

@login_required
def request_session(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        SessionRequest.objects.create(
            learner=request.user,
            skill=skill,
            message=message
        )
        django_messages.success(request, f"Your request for '{skill.title}' has been sent!")
        return redirect('skill_detail', pk=skill_id)
    return redirect('skill_detail', pk=skill_id)

@login_required
def request_list(request):
    # Incoming requests for providers
    incoming_requests = SessionRequest.objects.filter(skill__provider=request.user).order_by('-created_at')
    # Outgoing requests for learners
    outgoing_requests = SessionRequest.objects.filter(learner=request.user).order_by('-created_at')
    
    return render(request, 'bookings/request_list.html', {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests
    })

@login_required
def respond_request(request, request_id, action):
    session_request = get_object_or_404(SessionRequest, id=request_id, skill__provider=request.user)
    
    if action == 'accept':
        session_request.status = 'ACCEPTED'
        django_messages.success(request, "Request accepted!")
    elif action == 'reject':
        session_request.status = 'REJECTED'
        django_messages.warning(request, "Request rejected.")
    
    session_request.save()
    return redirect('request_list')
