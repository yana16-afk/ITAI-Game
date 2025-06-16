import re
from unidecode import unidecode

def load_corpus(filepath):
    sentences = []
    skipped = 0
    print(f"[DEBUG] Loading: {filepath}")
    try:
        with open("tgl_community_2017/filipino_rhyming_sawikain.txt", 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^\s*\d+\s*[:\-–]?\s*(.+)', line.strip())
                if match:
                    text = match.group(1).lower()
                    words = re.findall(r'\b\w+\b', unidecode(text))
                    if len(words) >= 2 and not all(word.isdigit() for word in words):
                        sentences.append(words)
                    else:
                        skipped += 1
        print(f"[DEBUG] Loaded {len(sentences)} valid phrases. Skipped: {skipped}")
    except FileNotFoundError:
        print("[ERROR] Corpus file not found.")
    return sentences

def load_word(filepath):
    try:
        with open("tgl_community_2017/Filipino-wordlist.txt", 'r', encoding='utf-8') as f:
            words = {
                word.strip().lower()
                for word in f
                if word.strip().isalpha() and len(word.strip()) > 1
            }
            print(f"[DEBUG] Loaded {len(words)} valid words.")
            return words
    except FileNotFoundError:
        print("[ERROR] Word list not found.")
        return set()

def rhyme_match(word, target_suffix):
    return isinstance(word, str) and word.endswith(target_suffix)
