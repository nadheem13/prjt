import os
import json
# import openai # Uncomment if you install openai package

def get_ai_response(user_message):
    """
    Get response from OpenAI or Mock.
    """
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if api_key:
        try:
            # Placeholder for actual OpenAI call
            # client = openai.OpenAI(api_key=api_key)
            # response = client.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": "user", "content": user_message}]
            # )
            # return response.choices[0].message.content
            return f"OpenAI Mock (Key found but package not installed): You asked '{user_message}'. I suggest looking for carpentry skills."
        except Exception as e:
            return f"Error connecting to AI: {str(e)}"
    else:
        # Mock Response Logic
        lower_msg = user_message.lower()
        if "carpentry" in lower_msg:
            return "Carpentry is a great skill! You'll need a hammer, wood, and a mentor. Check out our 'Woodworking 101' listings."
        elif "knit" in lower_msg or "sew" in lower_msg:
            return "For knitting or sewing, you need patience and good needles. We have several grandmothers offering lessons near you!"
        elif "cook" in lower_msg:
            return "Cooking traditional meals preserves culture. Search for 'Grandma's Recipes' in the skills section."
        else:
            return "That sounds interesting! Search our skills database or ask a Provider for more guidance."
