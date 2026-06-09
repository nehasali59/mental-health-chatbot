from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    # VADER sentiment scores
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    # Detect mood based on keywords first
    text_lower = text.lower()

    crisis_keywords = ['suicide', 'kill myself', 'end my life', 'want to die',
                      'hurt myself', 'self harm', 'no reason to live']

    anxious_keywords = ['anxious', 'anxiety', 'stressed', 'stress', 'worried',
                       'nervous', 'panic', 'overwhelmed', 'scared', 'fear']

    angry_keywords = ['angry', 'anger', 'furious', 'frustrated', 'hate',
                     'annoyed', 'irritated', 'mad', 'rage']

    sad_keywords = ['sad', 'depressed', 'depression', 'crying', 'hopeless',
                   'lonely', 'empty', 'worthless', 'miserable', 'unhappy']

    # Check crisis first
    for keyword in crisis_keywords:
        if keyword in text_lower:
            return {
                'sentiment': 'Crisis',
                'mood_score': -1.0,
                'compound': compound,
                'is_crisis': True
            }

    # Check other moods
    for keyword in anxious_keywords:
        if keyword in text_lower:
            return {
                'sentiment': 'Anxious',
                'mood_score': round(compound, 3),
                'compound': compound,
                'is_crisis': False
            }

    for keyword in angry_keywords:
        if keyword in text_lower:
            return {
                'sentiment': 'Angry',
                'mood_score': round(compound, 3),
                'compound': compound,
                'is_crisis': False
            }

    for keyword in sad_keywords:
        if keyword in text_lower:
            return {
                'sentiment': 'Sad',
                'mood_score': round(compound, 3),
                'compound': compound,
                'is_crisis': False
            }

    # Use compound score for remaining cases
    if compound >= 0.05:
        sentiment = 'Happy'
    elif compound <= -0.05:
        sentiment = 'Sad'
    else:
        sentiment = 'Neutral'

    return {
        'sentiment': sentiment,
        'mood_score': round(compound, 3),
        'compound': compound,
        'is_crisis': False
    }