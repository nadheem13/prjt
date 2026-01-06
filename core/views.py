from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from skills.models import Skill
from .ai_service import get_ai_response

def home(request):
    featured_skills = Skill.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/home.html', {'featured_skills': featured_skills})

def register(request):
    if request.method == 'POST':
        print(f"[VIEW DEBUG] POST keys: {request.POST.keys()}")
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            print("[VIEW DEBUG] Form valid. Saving...")
            user = form.save()
            print(f"[VIEW DEBUG] User {user.username} created.")
            login(request, user)
            return redirect('home')
        else:
            print(f"[VIEW DEBUG] FORM ERRORS: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    from bookings.models import SessionRequest
    incoming_requests = SessionRequest.objects.filter(skill__provider=request.user).order_by('-created_at')[:5]
    outgoing_requests = SessionRequest.objects.filter(learner=request.user).order_by('-created_at')[:5]
    
    return render(request, 'core/dashboard.html', {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests
    })

def ai_advisor(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            response = get_ai_response(user_message)
            return JsonResponse({'response': response})
        return JsonResponse({'error': 'No message provided'}, status=400)
    return render(request, 'core/ai_advisor.html')
