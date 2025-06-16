from collections import defaultdict, Counter

class BigramLanguageModel:
    def __init__(self):
        self.bigrams = defaultdict(Counter)
        self.vocab = set()

    def train(self, sentences):
        for phrase in sentences:
            for w1, w2 in zip(['<s>'] + phrase, phrase + ['</s>']):
                self.bigrams[w1][w2] += 1
                self.vocab.update([w1, w2])

    def predict(self, prev_word):
        candidates = self.bigrams[prev_word]
        total = sum(candidates.values()) + len(self.vocab)  # Laplace smoothing
        return {word: (candidates[word] + 1) / total for word in self.vocab}
