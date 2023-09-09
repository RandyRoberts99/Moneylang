
from compiler import ast, parser, code_gen, lexer

def __main__():

    newLexer = lexer("money_input.txt")
    newLexer.tokenize()

    parser = parser(newLexer.tokens)
    parser.parse_to_program()