
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.code_gen import Code_Gen
from compiler.vm import VM

def main():

    lexer = Lexer("money_input.txt")
    lexer.tokens = lexer.tokenize()

    print(lexer.tokens)

    parser = Parser(lexer.tokens)
    program_ast = parser.create_program()
    print(program_ast)

    #code_gen = Code_Gen(program_ast)
    #code_gen.generate_code()
    #print(code_gen.code_seq)

    #vm = VM(code_gen.code_seq)
    #vm.run()

if __name__ == "__main__":
    main()