from django.test import TestCase
from django.contrib.auth import get_user_model
from skills.models import Skill
from bookings.models import SessionRequest

User = get_user_model()

class UserFlowTests(TestCase):
    def setUp(self):
        # Create Provider
        self.provider = User.objects.create_user(
            username='grandpa_joe',
            password='password123',
            is_provider=True,
            is_learner=False
        )
        
        # Create Learner
        self.learner = User.objects.create_user(
            username='student_sally',
            password='password123',
            is_provider=False,
            is_learner=True
        )



    def test_form_direct(self):
        """Test form validation directly."""
        from .forms import CustomUserCreationForm
        data = {
            'username': 'direct_test_user',
            'email': 'direct@example.com',
            'password1': 'ComplexP@ssw0rd123!',
            'password2': 'ComplexP@ssw0rd123!',
            'is_provider': True,
            'is_learner': False,
            'bio': 'Test bio'
        }
        form = CustomUserCreationForm(data=data)
        if not form.is_valid():
            print("\n[DEBUG] Direct Form Errors:", form.errors)
        self.assertTrue(form.is_valid())
        print("\n[PASS] Direct Form Validation passed.")

    def test_provider_can_create_skill(self):
        """Test that a provider can create a skill."""
        skill = Skill.objects.create(
            provider=self.provider,
            title='Woodworking 101',
            description='Learn to make a birdhouse.',
            location='Community Center',
            availability='Weekends'
        )
        self.assertEqual(Skill.objects.count(), 1)
        self.assertEqual(skill.provider, self.provider)
        print("\n[PASS] Provider created skill successfully.")

    def test_learner_can_request_session(self):
        """Test that a learner can request a session for a skill."""
        skill = Skill.objects.create(
            provider=self.provider,
            title='Knitting',
            description='Basics of knitting.',
            location='Library',
            availability='Mondays'
        )
        
        request = SessionRequest.objects.create(
            learner=self.learner,
            skill=skill,
            message="I'd love to learn!"
        )
        
        self.assertEqual(SessionRequest.objects.count(), 1)
        self.assertEqual(request.status, 'PENDING')
        self.assertEqual(request.learner, self.learner)
        print("\n[PASS] Learner requested session successfully.")

    def test_user_registration_fields(self):
        """Test that custom fields are saved correctly."""
        user = User.objects.get(username='grandpa_joe')
        self.assertTrue(user.is_provider)
    def test_chat_creation(self):
        """Test that users can send messages to each other."""
        from bookings.models import Message
        self.client.login(username='student_sally', password='password123')
        # Correct URL for booking chat
        response = self.client.post(f'/bookings/chat/{self.provider.id}/', {'content': 'Hello Grandpa Joe!'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(sender=self.learner, receiver=self.provider, content='Hello Grandpa Joe!').exists())
        print("\n[PASS] Message created successfully via POST.")

        # Verify chat list shows the provider
        response = self.client.get('/bookings/chat/')
        self.assertContains(response, 'grandpa_joe')
        print("\n[PASS] Chat list contains the conversation user.")
