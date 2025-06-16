from flask import Flask, render_template, request, jsonify
from checker import load_corpus, rhyme_match, load_word
from AImodel import BigramLanguageModel
from AILogic import TugmaTikAI
import random

app = Flask(__name__)

sentences = load_corpus("tgl_community_2017/filipino_rhyming_sawikain.txt")
valid_words = load_word("tgl_community_2017/Filipino-wordlist.txt")

model = BigramLanguageModel()
model.train(sentences)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    difficulty = request.json.get("difficulty", "Katamtaman").split()[0]
    eligible = [s for s in sentences if len(s) >= 2]
    phrase = random.choice(eligible)
    prompt = phrase[:-1]
    answer = phrase[-1]
    suffix = answer[-3:]
    context = prompt[-1]
    return jsonify({
        "prompt": " ".join(prompt),
        "suffix": suffix,
        "context": context,
        "answer": answer
    })

@app.route("/play", methods=["POST"])
def play_round():
    data = request.json
    context = data["context"]
    suffix = data["suffix"]
    user_word = data["user_word"].strip().lower()
    difficulty = data.get("difficulty", "Katamtaman").split()[0] 

    ai = TugmaTikAI(model, difficulty=difficulty)
    ai_word = ai.choose_word(context, suffix)
    ai_rhyme_ok = rhyme_match(ai_word, suffix)

    if not user_word or not user_word.isalpha() or user_word not in valid_words or len(user_word) <= 1:
        return jsonify({
            "error": "Invalid word. Please enter a real Filipino word.",
            "user_rhyme": False,
            "ai_word": ai_word,
            "ai_rhyme": ai_rhyme_ok
        })

    user_rhyme_ok = rhyme_match(user_word, suffix)
    return jsonify({
        "user_rhyme": user_rhyme_ok,
        "ai_word": ai_word,
        "ai_rhyme": ai_rhyme_ok
    })

if __name__ == "__main__":
    app.run(debug=True)
