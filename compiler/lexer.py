# I didn't realize that my language would make lexing so easy LOL.

class Lexer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tokens = []

    def tokenize(self):
        words = []
        with open(self.file_name, 'r') as file:
            for line in file:
                word_list = line.strip().split(' ')
                for word in word_list:
                    for char in word:
                        if char != '💰' and char != ' ':
                            raise Exception("Invalid character exception")
                    words.append(word)
        return words