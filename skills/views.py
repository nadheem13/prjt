from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Skill
from .forms import SkillForm
from bookings.models import SessionRequest

def skill_list(request):
    skills = Skill.objects.all().order_by('-created_at')
    return render(request, 'skills/skill_list.html', {'skills': skills})

def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    existing_request = None
    if request.user.is_authenticated:
        existing_request = SessionRequest.objects.filter(learner=request.user, skill=skill).first()
    return render(request, 'skills/skill_detail.html', {
        'skill': skill,
        'existing_request': existing_request
    })

@login_required
def skill_create(request):
    if not request.user.is_provider:
        return redirect('home')
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.provider = request.user
            skill.save()
            return redirect('skill_detail', pk=skill.pk)
    else:
        form = SkillForm()
    return render(request, 'skills/skill_form.html', {'form': form})

@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    # Permission check: Only the provider can edit their own skill
    if skill.provider != request.user:
        return redirect('skill_detail', pk=pk)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skill_detail', pk=skill.pk)
    else:
        form = SkillForm(instance=skill)
    
    return render(request, 'skills/skill_form.html', {'form': form, 'skill': skill, 'is_edit': True})
