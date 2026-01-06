import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lost_skills.settings')
django.setup()

from core.forms import CustomUserCreationForm

data = {
    'username': 'debug_user',
    'email': 'debug@example.com',
    'password1': 'TestPass123!',
    'password2': 'TestPass123!',
    'is_provider': True,
    'bio': 'Debug bio'
}

form = CustomUserCreationForm(data=data)
if form.is_valid():
    print("Form is VALID")
else:
    print("Form ERRORS:", form.errors)
