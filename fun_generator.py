import random

class FunGenerator:
    def __init__(self, data=[]):
        self.data = data

    def generate(self, data):
        words_count = len(data)
        if words_count > 10:
            text_words_count = random.randint(2, 6)
            text = []
            for i in range(text_words_count):
                text.append(str(data[random.randint(0, words_count - 1)] + " "))
            return ''.join(text)
        else:
            pass
