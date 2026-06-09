from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from database import db, User, ChatHistory
from sentiment import analyze_sentiment
from chatbot import get_chatbot_response
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mindease_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error='Email already registered')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('chat'))
        return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
    chats = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp).all()
    return render_template('chat.html', chats=chats, username=current_user.username)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message.strip():
        return jsonify({'error': 'Empty message'}), 400

    # Analyze sentiment
    sentiment_result = analyze_sentiment(user_message)
    sentiment = sentiment_result['sentiment']
    mood_score = sentiment_result['mood_score']
    is_crisis = sentiment_result['is_crisis']

    # Get bot response
    bot_response = get_chatbot_response(user_message, sentiment)

    # Add crisis message if needed
    if is_crisis:
        bot_response += "\n\n🆘 If you are in crisis please contact iCall: 9152987821 or Vandrevala Foundation: 1860-2662-345. You are not alone."

    # Save to database
    chat = ChatHistory(
        user_id=current_user.id,
        message=user_message,
        response=bot_response,
        sentiment=sentiment,
        mood_score=mood_score
    )
    db.session.add(chat)
    db.session.commit()

    return jsonify({
        'response': bot_response,
        'sentiment': sentiment,
        'is_crisis': is_crisis
    })

@app.route('/dashboard')
@login_required
def dashboard():
    chats = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp).all()

    mood_data = {}
    for chat in chats:
        date = chat.timestamp.strftime('%a')
        if date not in mood_data:
            mood_data[date] = []
        mood_data[date].append(chat.mood_score)

    avg_mood = {day: round(sum(scores)/len(scores), 2) for day, scores in mood_data.items()}

    sentiment_counts = {}
    for chat in chats:
        sentiment_counts[chat.sentiment] = sentiment_counts.get(chat.sentiment, 0) + 1

    total_sessions = len(chats)
    positive_count = sentiment_counts.get('Happy', 0)
    positive_pct = round((positive_count / total_sessions * 100), 1) if total_sessions > 0 else 0

    return render_template('dashboard.html',
        username=current_user.username,
        chats=chats[-5:],
        avg_mood=avg_mood,
        sentiment_counts=sentiment_counts,
        total_sessions=total_sessions,
        positive_pct=positive_pct
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)