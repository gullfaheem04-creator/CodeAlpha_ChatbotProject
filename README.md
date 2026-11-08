# CodeAlpha_ChatbotProject

AI-powered customer-support chatbot ("Brewie") for a demo coffee-subscription website (BrewBox).
Built for **CodeAlpha Cloud Computing Internship, Task 4: Making a Chatbot**.

## Features
- Retrieval-based NLP model: TF-IDF (word + character n-grams) with cosine similarity
- Instant answers through a Flask REST API (`POST /api/chat`)
- Floating chat widget integrated into the website (HTML, CSS, vanilla JS)
- Handles typos, filler words and off-topic questions (confidence threshold + fallback)
- Quick-reply suggestion chips for better engagement
- Unanswered questions are logged to `logs/unanswered.csv` so you can improve the training data
- Accuracy test script (`tests/evaluate.py`) on unseen sentences
- Ready for cloud deployment (`Procfile`, `gunicorn`)

## Project structure
```
app.py            Flask server and API
chatbot.py        NLP engine
intents.json      Training data (patterns, responses, suggestions)
templates/        Website HTML
static/           CSS and chat widget JS
tests/evaluate.py Accuracy test
```

## Run locally
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 and click **Ask Brewie**.

## Test accuracy
```bash
python tests/evaluate.py
```

## API
`POST /api/chat` with `{"message": "how long does delivery take?"}`
```json
{"tag": "delivery_time", "confidence": 1.0, "response": "...", "suggestions": ["Track my order"]}
```

## Deploy to the cloud (Render, free tier)
1. Push this repo to GitHub.
2. On render.com: New > Web Service > connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy and share the public URL.

## Add your own business
Edit `intents.json`: add an intent with a `tag`, several `patterns` (example user questions),
`responses` and optional `suggestions`. Restart the server. No retraining step is needed.

## Tech stack
Python, Flask, scikit-learn, HTML/CSS/JavaScript, Gunicorn
