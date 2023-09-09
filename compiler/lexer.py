# I didn't realize that my language would make lexing so easy LOL.

class Lexer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tokens = []

    def tokenize(self):
        with open(self.file_name, "r") as file:
            for line in file:
                words = line.split(' ')
                for word in words:

                    for char in word:
                        if char != '💰' and char != ' ':
                            print("Invalid character: " + char)
                            exit(1)
                    self.tokens.append(word)