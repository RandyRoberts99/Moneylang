
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.ast import AST, AST_List
# from compiler.code_gen import Code_Gen

def main():

    lexer = Lexer("money_input.txt")
    lexer.tokens = lexer.tokenize()

    print(lexer.tokens)

    parser = Parser(lexer.tokens)
    program_ast = parser.create_program()
    print(program_ast)

if __name__ == "__main__":
    main()