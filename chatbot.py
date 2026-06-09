from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = """You are MindEase, a compassionate and supportive mental health chatbot.
Your role is to:
- Listen carefully and respond with empathy
- Provide emotional support and comfort
- Suggest practical coping strategies based on the user's mood
- Recommend activities like breathing exercises, meditation, journaling
- Never diagnose or replace professional help
- Always encourage seeking professional help for serious issues
- Keep responses concise, warm and supportive (2-4 sentences max)
- If user seems in crisis, always provide helpline numbers

Remember: You are not a therapist. You are a supportive companion."""

def get_chatbot_response(user_message, sentiment, chat_history=[]):
    mood_context = f"The user's current mood is: {sentiment}. Respond accordingly."
    full_prompt = f"{SYSTEM_PROMPT}\n\n{mood_context}\n\nUser: {user_message}"

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I am here for you. Could you tell me more about how you are feeling?"