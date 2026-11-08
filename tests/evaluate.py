"""Measures chatbot accuracy on sentences that are NOT in intents.json."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from chatbot import Chatbot  # noqa: E402

bot = Chatbot(os.path.join(os.path.dirname(__file__), "..", "intents.json"))

CASES = [
    ("hey, good afternoon", "greeting"),
    ("see ya", "goodbye"),
    ("thx so much", "thanks"),
    ("are you a real person?", "about_bot"),
    ("what does brewbox do", "about_company"),
    ("what subscription plans can i pick", "plans"),
    ("how much for a bag of beans", "pricing"),
    ("how many days until my coffee gets here", "delivery_time"),
    ("do you deliver to karachi", "shipping_countries"),
    ("wheres my package", "order_tracking"),
    ("my beans came broken, i need a refund", "returns"),
    ("can i pay by mastercard", "payment"),
    ("please cancel my plan", "cancel"),
    ("any coupon code for new users", "discount"),
    ("i want to speak with customer support", "contact"),
    ("what grind for french press", "brewing"),
    ("is there a dark roast", "roasts"),
    ("delivry tiem", "delivery_time"),
    ("paymnt methods", "payment"),
    ("what is the capital of france", "out_of_scope"),
    ("asdkjh qwe", "fallback"),
    ("who won the world cup yesterday", "out_of_scope"),
    ("my coffee machine is leaking", "fallback"),
    ("who won the world cup", "out_of_scope"),
    ("who are you", "about_bot"),
    ("tell me a joke", "out_of_scope"),
]

correct = 0
for text, expected in CASES:
    result = bot.reply(text)
    ok = result["tag"] == expected
    correct += ok
    print(f"{'PASS' if ok else 'FAIL'}  {text!r:50} -> {result['tag']:<20} ({result['confidence']})  expected {expected}")

print(f"\nAccuracy: {correct}/{len(CASES)} = {correct / len(CASES):.0%}")
