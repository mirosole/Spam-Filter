import os
import re
from collections import Counter
from confmat import BinaryConfusionMatrix
from corpus import Corpus
from quality import compute_quality_for_corpus

class MyFilter:
    chars = [">", "-", "*", "|", "--", "&", "'", '"', "(", ")"]

    def __init__(self):
        self.trained = False
        self.matrix = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
        self.spam_words = Counter()
        self.ok_words = Counter()
        self.stop_words = {"the", "and", "in", "to", "of", "a", "for", "on", "with", "at"}

    def train(self, train_corpus_dir):
        spam_count, ok_count = 0, 0

        for filename, body in Corpus(train_corpus_dir).emails():
            if filename.startswith('SPAM'):
                spam_count += 1
                self.update_word_frequency(body, self.spam_words)
            elif filename.startswith('OK'):
                ok_count += 1
                self.update_word_frequency(body, self.ok_words)

        self.normalize_word_frequency(self.spam_words, spam_count)
        self.normalize_word_frequency(self.ok_words, ok_count)

        self.trained = True

    def update_word_frequency(self, email, word_frequency):
        words = self.preprocess(email)
        word_frequency.update(words)

    def normalize_word_frequency(self, word_frequency, total_count):
        for word in word_frequency:
            word_frequency[word] /= total_count

    def preprocess(self, sentence):
        # Replace repeating characters (more than 2 times) with a single character
        sentence = re.sub(r'(\S)\1{2,}', r'\1', sentence)
        # Replace other symbols
        sentence = re.sub(r'[">*|&\'"()]', ' ', sentence)
        
        # Word generator for improved performance
        words = (word.lower() for word in re.findall(r'\b\w+\b', sentence) if word.lower() not in self.stop_words)

        # Apply extended Porter stemming rules
        words = [self.porter_stemmer(word) for word in words]

        return words

    def porter_stemmer(self, word):
        # Simple implementation of extended Porter stemming rules
        if word.endswith('ing'):
            return word[:-3]
        elif word.endswith('ly'):
            return word[:-2]
        elif word.endswith('ed'):
            return word[:-2]
        elif word.endswith('es'):
            return word[:-2]
        elif word.endswith('s'):
            return word[:-1]
        elif word.endswith('er'):
            return word[:-2]
        elif word.endswith('ly'):
            return word[:-2]
        return word

    def has_repeating_chars(self, text):
        for char in self.chars:
            if char * 4 in text:
                return True
        return False

    def has_many_empty_lines(self, text, threshold=5):
        empty_lines = 0
        for line in text.split('\n'):
            if not line.strip():
                empty_lines += 1
                if empty_lines >= threshold:
                    return True
            else:
                empty_lines = 0
        return False

    def is_spam(self, email):
        # Check for the presence of many empty lines
        has_empty_lines = self.has_many_empty_lines(email)

        spam_score = 0

        # Evaluate "spam score" for words
        words = self.preprocess(email)
        for word in words:
            if len(word) > 2:
                spam_score += self.spam_words.get(word, 0)

        # Check for the presence of repeating characters
        has_repeating_chars = self.has_repeating_chars(email)
        if has_repeating_chars:
            spam_score += 1  # Increase "spam score"

        # Check for the presence of words frequently seen in spam
        spam_keywords = {'free', 'money'}  # Add your own keywords
        if any(keyword in words for keyword in spam_keywords):
            spam_score += 1

        # Make the final decision
        return has_empty_lines or has_repeating_chars or spam_score > 0

    def test(self, test_corpus_dir):
        predictions = {}
        for filename, body in Corpus(test_corpus_dir).emails():
            prediction = 'SPAM' if self.is_spam(body) else 'OK'
            predictions[filename] = prediction
            truth = 'SPAM' if filename.startswith('SPAM') else 'OK'
            self.matrix.update(truth, prediction)

        output_path = os.path.join(test_corpus_dir, r'!prediction.txt')
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for filename, prediction in predictions.items():
                output_file.write(f"{filename} {prediction}\n")

        # Output metrics
        print("Confusion Matrix:")
        print(self.matrix.as_dict())

if __name__ == "__main__":
    my_filter = MyFilter()
    my_filter.train('C:/Microsoft VS Code/codes/mirosole_spamfiltr/1')
    my_filter.test('C:/Microsoft VS Code/codes/mirosole_spamfiltr/2')
    corpus_dir = 'C:/Microsoft VS Code/codes/mirosole_spamfiltr/2'
    quality = compute_quality_for_corpus(corpus_dir)
    print(f"Quality Score: {quality}")
