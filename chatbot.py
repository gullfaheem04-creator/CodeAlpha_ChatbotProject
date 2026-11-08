"""Retrieval-based chatbot engine (TF-IDF + cosine similarity).

How it works
1. Every training pattern in intents.json is turned into two TF-IDF vectors:
   word n-grams (meaning) and character n-grams (tolerates typos).
2. A user message is vectorised the same way and compared with every pattern.
3. The intent of the best-matching pattern is returned if its score passes a
   confidence threshold, otherwise the bot falls back to a safe default reply.
"""
import json
import random
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


STOP_WORDS = {
    "a", "an", "the", "is", "are", "am", "was", "of", "to", "do", "does", "did", "i", "you",
    "my", "me", "your", "can", "what", "how", "it", "in", "on", "for", "with", "and", "or",
    "please", "there", "any", "have", "be", "get", "gets", "would", "like", "want", "so",
    "who", "much", "many", "that", "this", "about", "will", "should", "we", "us", "if", "at", "some",
}


def normalize(text: str) -> str:
    """Lower-case, strip punctuation and remove filler words.
    Falls back to the cleaned text when only filler words are left (e.g. 'hi')."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    words = text.split()
    kept = [w for w in words if w not in STOP_WORDS]
    return " ".join(kept or words)


class Chatbot:
    def __init__(self, intents_path="intents.json", threshold=0.30):
        data = json.loads(Path(intents_path).read_text(encoding="utf-8"))
        self.intents = {i["tag"]: i for i in data["intents"]}
        self.fallback = data["fallback"]
        self.fallback_suggestions = data.get("fallback_suggestions", [])
        self.threshold = threshold

        self.patterns, self.tags = [], []
        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                self.patterns.append(normalize(pattern))
                self.tags.append(intent["tag"])

        self.word_vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)
        self.word_matrix = self.word_vec.fit_transform(self.patterns)
        self.char_matrix = self.char_vec.fit_transform(self.patterns)

    def predict(self, message: str):
        """Return (tag, confidence). tag is None when confidence is too low."""
        query = normalize(message)
        if not query:
            return None, 0.0
        word_sim = cosine_similarity(self.word_vec.transform([query]), self.word_matrix)[0]
        char_sim = cosine_similarity(self.char_vec.transform([query]), self.char_matrix)[0]
        scores = 0.5 * word_sim + 0.5 * char_sim
        best = int(scores.argmax())
        confidence = float(scores[best])
        if confidence < self.threshold:
            return None, confidence
        return self.tags[best], confidence

    def reply(self, message: str) -> dict:
        tag, confidence = self.predict(message)
        if tag is None:
            return {
                "tag": "fallback",
                "confidence": round(confidence, 3),
                "response": random.choice(self.fallback),
                "suggestions": self.fallback_suggestions,
            }
        intent = self.intents[tag]
        return {
            "tag": tag,
            "confidence": round(confidence, 3),
            "response": random.choice(intent["responses"]),
            "suggestions": intent.get("suggestions", []),
        }
