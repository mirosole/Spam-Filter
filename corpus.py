# corpus.py
import os

class Corpus:
    def __init__(self, directory):
        self.directory = directory

    def emails(self):
        for filename in os.listdir(self.directory):
            if not filename.startswith('!'):
                with open(os.path.join(self.directory, filename), 'r', encoding='utf-8') as file:
                    body = file.read()
                    yield filename, body