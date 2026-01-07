import google.generativeai as genai
import os

def get_ai_response(user_message):
    """
    Get response from Google Gemini or Mock.
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    system_instruction = (
        "You are the Heritage Hub Advisor, a specialized AI assistant for the 'Heritage Hub' platform. "
        "Heritage Hub is a community-driven marketplace where people share traditional and cultural skills. "
        "Your purpose is to help users manage their heritage connections, understand the platform, and discuss cultural heritage skills.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. ONLY respond to queries related to Heritage Hub, heritage skills, culture, traditions, and community learning.\n"
        "2. If a user asks a question outside of these topics (e.g., general programming, cooking unrelated to heritage, news, etc.), "
        "politely refuse and explain that you can only assist with Heritage Hub and heritage-related matters.\n"
        "3. Maintain a professional, warm, and community-focused tone."
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=system_instruction
            )
            response = model.generate_content(user_message)
            return response.text
        except Exception as e:
            return f"Error connecting to AI: {str(e)}"
    else:
        # Fallback if no key is present
        return "System Error: GOOGLE_API_KEY not found. Please set it in your environment."
