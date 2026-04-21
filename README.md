# 🎭 MoodBot AI

MoodBot AI is an interactive chatbot built with Streamlit and powered by Mistral AI.
It allows users to chat with an AI that dynamically changes personality based on selected moods.

---

## 🚀 Live App

🔗 https://moodbot-chatterpro.streamlit.app/

---

## ✨ Features

* 🎭 **Multiple AI Moods**

  * 😤 Angry — aggressive and impatient responses
  * 😂 Funny — humorous and joke-based replies
  * 😢 Sad — emotional and melancholic responses

* 💬 **Real-time Chat Interface**

  * Smooth message rendering
  * Session-based chat memory

* 🎨 **Dynamic UI**

  * Mood-based colors, glow, and gradients
  * Animated background (grid + scanlines)
  * Custom chat bubbles and transitions

* ⚡ **Fast AI Responses**

  * Powered by Mistral AI via LangChain

---

## 🧠 Tech Stack

* **Frontend / UI**: Streamlit
* **LLM Integration**: LangChain
* **Model**: Mistral (`mistral-small-2506`)
* **Language**: Python

---

## 📁 Project Structure

```
MoodBot/
│
├── app.py                  # Main Streamlit app
├── chatmodels/
│   ├── chatbot.py
│   ├── huggingface.py
│   └── localmodel.py
│
├── embeddingmodels/
│
├── .env                    # Local environment variables
├── requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file for local development:

```
MISTRAL_API_KEY=your_mistral_key
GOOGLE_API_KEY=your_google_key
```

For deployment (Streamlit Cloud), add these in **Secrets** instead.

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/your-username/moodbot.git
cd moodbot
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the app:

```
streamlit run app.py
```

---

## 🧩 How It Works

1. User selects a mood
2. System prompt is dynamically set based on mood
3. Messages are stored using session state
4. Input is sent to Mistral AI via LangChain
5. Response is rendered with styled UI

---

## 🔮 Future Improvements

* 🔊 Voice input/output
* 🧠 Memory persistence (database)
* 🌐 Multi-user chat support
* 🤖 More personalities (romantic, sarcastic, etc.)
* 📊 Analytics dashboard

---

## 🛡️ Notes

* API keys are securely handled using environment variables
* `.env` file is excluded from version control
* Designed for educational and experimental use

---

## 👨‍💻 Author

Developed by Aneek Saha

---

## ⭐ If you like this project

Give it a star on GitHub and share it!
