class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.symbols = {}
        self.program = []
        self.ip = 0  # Instruction pointer

    def load_program(self, program):
        self.program = program

    def run(self):
        while self.ip < len(self.program):
            opcode = self.program[self.ip]

            if opcode == "PUSH":
                self.ip += 1
                value = self.program[self.ip]
                self.stack.append(value)

            elif opcode == "ADD":
                a = self.stack.pop()
                b = self.stack.pop()
                result = a + b
                self.stack.append(result)

            elif opcode == "SUB":
                a = self.stack.pop()
                b = self.stack.pop()
                result = b - a
                self.stack.append(result)

            elif opcode == "MUL":
                a = self.stack.pop()
                b = self.stack.pop()
                result = a * b
                self.stack.append(result)

            elif opcode == "DIV":
                a = self.stack.pop()
                b = self.stack.pop()
                if a == 0:
                    raise ValueError("Division by zero")
                result = b / a
                self.stack.append(result)

            elif opcode == "MOD":
                a = self.stack.pop()
                b = self.stack.pop()
                if a == 0:
                    raise ValueError("Division by zero")
                result = b % a

            elif opcode == "ASSIGN":
                variable_name = self.program[self.ip + 1]
                value = self.stack.pop()
                self.memory[variable_name] = value
                self.ip += 1

            elif opcode == "PRINT":
                variable_name = self.program[self.ip + 1]
                value = self.memory.get(variable_name)
                if value is not None:
                    print(value)
                else:
                    raise ValueError(f"Variable '{variable_name}' not found.")

            elif opcode == "HALT":
                break

            self.ip += 1

    def generate_code(self, code):
        # Generate code and store it in the program
        self.program.extend(code)

    def define_symbol(self, symbol_name, value):
        # Define a symbol in the symbol table
        self.symbols[symbol_name] = value

    def lookup_symbol(self, symbol_name):
        # Look up a symbol in the symbol table
        return self.symbols.get(symbol_name)


# Example usage:
vm = VirtualMachine()

# Generate code with different variable types
code = [
    "PUSH", 5,          # Push an integer
    "PUSH", 3.0,        # Push a float
    "ADD",              # Add float and integer
    "ASSIGN", "x",      # Assign the result to 'x'
    "PUSH", "Hello",    # Push a string
    "ASSIGN", "str_var",# Assign a string
    "PUSH", True,       # Push a boolean
    "ASSIGN", "bool_var",# Assign a boolean
    "PRINT", "x",       # Print 'x'
    "PRINT", "str_var", # Print a string
    "PRINT", "bool_var",# Print a boolean
    "HALT",
]

vm.generate_code(code)
vm.run()
