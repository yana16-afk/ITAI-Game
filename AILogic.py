import random

class TugmaTikAI:
    def __init__(self, model, difficulty='Katamtaman'):
        self.model = model
        self.difficulty = difficulty

    def choose_word(self, prev_word, target_suffix):
        probs = self.model.predict(prev_word)
        vocab = list(probs.keys())

        rhyming_words = [word for word in vocab if word.endswith(target_suffix)]
        non_rhyming_words = [word for word in vocab if not word.endswith(target_suffix) and len(word) > 2]

        if self.difficulty == 'Madali':
            if non_rhyming_words:
                chosen = random.choice(non_rhyming_words)
                print(f"[DEBUG] Madali AI picked non-rhyme: {chosen}")
                return chosen
            else:
                fallback = random.choice(vocab)
                print(f"[DEBUG] Madali fallback: {fallback}")
                return fallback

        elif self.difficulty == 'Mahirap':
            if rhyming_words:
                def score(w): return probs[w] * 1.5 + (1.0 / (1 + len(w)))
                return max(rhyming_words, key=score)
            else:
                return max(probs, key=probs.get)

        else:  # Katamtaman
            if rhyming_words:
                return max(rhyming_words, key=lambda w: probs[w])
            else:
                return max(probs, key=probs.get)
