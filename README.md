# 🧠 MindEase — AI Mental Health Chatbot

A compassionate AI-powered mental health companion that chats with users, detects their emotional state in real time, and tracks mood patterns over time through an interactive dashboard.

---

## 🎯 What Makes This Different

Most chatbots just respond to text. MindEase goes further — it analyzes the **sentiment behind every message**, detects crisis situations automatically, and builds a **mood history dashboard** so users can understand their emotional patterns over time.

---

## 🚀 Features

- Secure user registration and login system
- Real-time chat with AI companion powered by Llama 3.3 via Groq API
- Sentiment detection on every message — Happy, Sad, Anxious, Angry, Neutral
- Mood tag shown after every user message
- Crisis detection — shows Indian helpline numbers if alarming message is detected
- Mood tracking dashboard with weekly graph
- Session statistics — total sessions, positive mood percentage, anxious and sad counts
- Recent mood history list
- Fully responsive dark UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| AI Model | Llama 3.3 70B (via Groq API) |
| Sentiment Analysis | VADER + TextBlob |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (via Flask-SQLAlchemy) |
| Authentication | Flask-Login + Flask-Bcrypt |
| Mood Graph | Chart.js |
| Version Control | GitHub |

---

## 📁 Project Structure

```
mental-health-chatbot/
│
├── app.py                  ← Main Flask application and all routes
├── database.py             ← SQLite database models (User, ChatHistory)
├── sentiment.py            ← Sentiment analysis using VADER and TextBlob
├── chatbot.py              ← Groq API integration with Llama 3.3
│
├── templates/
│   ├── base.html           ← Base HTML template
│   ├── login.html          ← Login page
│   ├── signup.html         ← Registration page
│   ├── chat.html           ← Main chat interface
│   └── dashboard.html      ← Mood tracking dashboard
│
├── static/
│   ├── style.css           ← Full app styling
│   └── script.js           ← Chat functionality and API calls
│
├── .env                    ← API keys (never pushed to GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/nehasali59/mental-health-chatbot.git
cd mental-health-chatbot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file**
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## 💡 How It Works

1. User registers and logs in securely
2. User types a message in the chat
3. VADER sentiment analyzer detects the mood from the message
4. Mood is sent as context to Llama 3.3 model via Groq API
5. Bot responds with empathy based on detected mood
6. Message, response, sentiment and mood score saved to SQLite database
7. Dashboard pulls all history and displays mood graph and statistics

---

## 🧠 Sentiment Detection

| Mood | Trigger |
|---|---|
| Happy | Positive compound score |
| Sad | Negative keywords or low compound score |
| Anxious | Keywords like anxious, stressed, worried, panic |
| Angry | Keywords like angry, frustrated, furious |
| Neutral | Compound score near zero |
| Crisis | Keywords like hurt myself, want to die, self harm |

---

## 🆘 Crisis Detection

If a user sends a message containing crisis keywords, the system:
- Immediately detects it as a Crisis sentiment
- Bot responds with extra care and compassion
- Automatically displays Indian mental health helplines:
  - **iCall:** 9152987821
  - **Vandrevala Foundation:** 1860-2662-345

---

## 📊 Dashboard Features

- Total chat sessions count
- Positive mood percentage
- Anxious and sad session counts
- Weekly mood score graph (Chart.js)
- Recent mood history with timestamps

---

## ⚠️ Limitations

- Sentiment detection based on keywords may miss complex emotional states
- Not a replacement for professional mental health support
- Crisis detection based on keyword matching — may miss indirect expressions
- Response quality depends on Groq API availability

---

## 🔮 Future Scope

- Add multilingual support for Hindi and other Indian languages
- Integrate voice input for more natural interaction
- Add guided meditation and breathing exercise modules
- Deploy on cloud platform for public access
- Improve sentiment detection using fine-tuned ML model
- Add weekly and monthly mood report generation

