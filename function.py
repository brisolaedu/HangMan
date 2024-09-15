import random

def get_word():
    words = []
    with open("static/words.txt") as file:
        for line in file:
            words.append(line.strip())
    
    word = words[random.randint(0, len(words) - 1)]
    return word
    