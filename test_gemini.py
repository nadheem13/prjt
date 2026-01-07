import google.generativeai as genai
import os
import dotenv
import sys

# Force utf-8 output
sys.stdout.reconfigure(encoding='utf-8')

dotenv.load_dotenv(encoding='utf-8')

api_key = os.environ.get('GOOGLE_API_KEY')
print(f"Key loaded: {api_key[:10]}...")

try:
    system_instruction = (
        "You are the Heritage Hub Advisor... [Restricted to Heritage Hub context]"
    )
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction="You are the Heritage Hub Advisor. Only discuss Heritage Hub and heritage skills."
    )
    # Test project query
    print("Testing Project Query: 'What is Heritage Hub?'")
    response = model.generate_content('What is Heritage Hub?')
    print(f"Response: {response.text}\n")
    
    # Test unrelated query
    print("Testing Unrelated Query: 'How to make a pizza?'")
    response = model.generate_content('How to make a pizza?')
    print(f"Response: {response.text}")
except Exception as e:
    print("Error detailed:")
    print(repr(e))
