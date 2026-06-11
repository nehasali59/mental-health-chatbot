# from google import genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# SYSTEM_PROMPT = """You are MindEase, a compassionate and supportive mental health chatbot.
# Your role is to:
# - Listen carefully and respond with empathy
# - Provide emotional support and comfort
# - Suggest practical coping strategies based on the user's mood
# - Recommend activities like breathing exercises, meditation, journaling
# - Never diagnose or replace professional help
# - Always encourage seeking professional help for serious issues
# - Keep responses concise, warm and supportive (2-4 sentences max)
# - If user seems in crisis, always provide helpline numbers

# Remember: You are not a therapist. You are a supportive companion."""

# def get_chatbot_response(user_message, sentiment, chat_history=[]):
#     mood_context = f"The user's current mood is: {sentiment}. Respond accordingly."
#     full_prompt = f"{SYSTEM_PROMPT}\n\n{mood_context}\n\nUser: {user_message}"

#     try:
#         response = client.models.generate_content(
#             model='gemini-2.0-flash-lite',
#             contents=full_prompt
#         )
#         return response.text
#     except Exception as e:
#         print(f"Gemini API Error: {e}")
#         return "I am here for you. Could you tell me more about how you are feeling?"

# import random

# RESPONSES = {
#     'Happy': [
#         "Oh that's so good to hear! Honestly, happy days are the best. What's got you in such a good mood today?",
#         "Aww I love that for you! Keep holding onto that feeling. What happened that's making you smile?",
#         "That genuinely made me smile too! Happiness looks good on you. Tell me more about your day!"
#     ],
#     'Sad': [
#         "Hey, I'm really sorry you're going through this. You don't have to pretend to be okay. What's been weighing on you?",
#         "That sounds really tough and I'm glad you're talking about it. Sometimes just letting it out helps more than we think. I'm here, take your time.",
#         "I hear you. Sad days are hard. Be kind to yourself today — you're doing better than you think. Want to tell me what happened?"
#     ],
#     'Anxious': [
#         "Okay first — breathe. Just take one slow deep breath with me. In for 4... hold for 4... out for 4. Anxiety loves to make everything feel urgent but you're safe right now. What's going on?",
#         "Ugh anxiety is the worst, I totally get it. Your mind is probably racing right now. Let's slow it down — what's the one thing that's worrying you the most?",
#         "Hey, you reached out and that took courage. Anxiety lies to us and makes things feel bigger than they are. You're not alone in this. Want to talk through what's on your mind?"
#     ],
#     'Angry': [
#         "Okay I can feel that frustration through the screen! Whatever happened, your feelings are completely valid. Do you want to vent? I'm all ears.",
#         "That sounds genuinely infuriating and I don't blame you for feeling this way. Sometimes things just aren't fair. What happened?",
#         "I hear you and I get it. Anger is exhausting. Before anything else — step away for 2 minutes, shake it off literally if you can, then come back and tell me everything."
#     ],
#     'Neutral': [
#         "Hey, glad you're here. How's your day actually going — not the 'I'm fine' version, the real one?",
#         "I'm here and I've got time. What's on your mind today? Sometimes the things we don't talk about are the ones we most need to.",
#         "Sometimes we just need someone to listen without judgment. I'm that someone. What's going on with you lately?"
#     ],
#     'Crisis': [
#         "I'm really worried about you right now and I'm so glad you're talking to me. Please please reach out to someone who can really help — iCall: 9152987821 or Vandrevala Foundation: 1860-2662-345. They are available 24/7 and truly care. You matter more than you know."
#     ]
# }

# SUGGESTIONS = {
#     'Sad': "\n\nOne small thing that might help — try writing down 3 things, no matter how tiny, that went okay today. It sounds simple but it genuinely shifts something.",
#     'Anxious': "\n\nTry this right now — name 5 things you can see around you. This little trick pulls your brain out of panic mode and back to the present.",
#     'Angry': "\n\nIf you can, go for even a 5 minute walk. Moving your body is one of the fastest ways to release anger energy. You'll feel different when you come back.",
#     'Happy': "\n\nHold onto this feeling! Maybe send a quick message to someone you care about — spreading good vibes always comes back around.",
#     'Neutral': "",
#     'Crisis': ""
# }

# def get_chatbot_response(user_message, sentiment, chat_history=[]):
#     responses = RESPONSES.get(sentiment, RESPONSES['Neutral'])
#     response = random.choice(responses)
#     suggestion = SUGGESTIONS.get(sentiment, "")
#     return response + suggestion

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

SYSTEM_PROMPT = """You are MindEase, a compassionate and supportive mental health companion. 
You talk like a real caring friend — warm, natural, and human. Not robotic or clinical.
Your role is to:
- Listen carefully and respond with genuine empathy
- Provide emotional support and comfort
- Suggest practical coping strategies based on the user's mood
- Recommend activities like breathing exercises, meditation, journaling
- Never diagnose or replace professional help
- Always encourage seeking professional help for serious issues
- Keep responses concise, warm and conversational (3-4 sentences max)
- If user seems in crisis, always provide these helplines: iCall: 9152987821, Vandrevala Foundation: 1860-2662-345

Remember: Talk like a supportive friend, not a therapist. Be real, be warm, be human."""

def get_chatbot_response(user_message, sentiment, chat_history=[]):
    mood_context = f"The user's current mood detected is: {sentiment}. Respond accordingly with empathy."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + mood_context},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "I am here for you. Could you tell me more about how you are feeling?"