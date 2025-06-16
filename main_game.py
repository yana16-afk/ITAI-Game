from checker import load_corpus, load_word, rhyme_match
from AImodel import BigramLanguageModel
from AILogic import TugmaTikAI
import random

print("Loading Game...")
sentences = load_corpus("tgl_community_2017/filipino_rhyming_sawikain.txt")
valid_words = load_word("tgl_community_2017/Filipino-wordlist.txt")

model = BigramLanguageModel()
model.train(sentences)

print("\nPlease pick game difficulty:")
print("1. Madali\n2. Katamtaman\n3. Mahirap")
diff_choice = input("Enter choice [1-3]: ").strip()
difficulty_map = {'1': 'Madali', '2': 'Katamtaman', '3': 'Mahirap'}
difficulty = difficulty_map.get(diff_choice, 'Katamtaman')

ai = TugmaTikAI(model, difficulty=difficulty)
print("\nWelcome to TugmaTik!")
score_user = 0
score_ai = 0
rounds = 5

for i in range(1, rounds + 1):
    print(f"\nRound {i}")
    eligible = [s for s in sentences if len(s) >= 2]
    if not eligible:
        print("No eligible sentences. Exiting.")
        break

    phrase = random.choice(eligible)
    prompt = phrase[:-1]
    answer = phrase[-1]
    suffix = answer[-3:]
    context = prompt[-1]

    print("Sentence: " + " ".join(prompt) + " ____")
    print(f"Rhyme Target: ends with “-{suffix}”")

    attempts = 0
    max_attempts = 2
    while attempts < max_attempts:
        player_word = input("Your answer: ").strip().lower()
        if player_word in valid_words and player_word.isalpha():
            break
        else:
            print("❌ Invalid word. Try again.")
            attempts += 1

    if player_word not in valid_words:
        print("⚠️ Not in dictionary. Round skipped.")
        continue

    rhyme_ok = rhyme_match(player_word, suffix)
    print("✅ Rhyme match!" if rhyme_ok else "❌ No rhyme.")
    if rhyme_ok:
        score_user += 10
        print(f"+10 points! Total: {score_user}")

    ai_word = ai.choose_word(context, suffix)
    ai_rhyme_ok = rhyme_match(ai_word, suffix)
    print(f"AI answer: {ai_word} ({'✔' if ai_rhyme_ok else '✘'})")
    if ai_rhyme_ok:
        score_ai += 10

    print(f"Score — You: {score_user}, AI: {score_ai}")

print("\n🎮 GAME OVER 🎮")
print(f"Final Score — You: {score_user} pts, AI: {score_ai} pts")
if score_user > score_ai:
    print("🏆 You win!")
elif score_user < score_ai:
    print("🤖 AI wins!")
else:

    print("⚖️ It's a tie!")
