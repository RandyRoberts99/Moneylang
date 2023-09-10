class VM:

    def __init__(self, code_seq):
        self.stack = []
        self.memory = {}
        self.program = code_seq
        self.ip = 0  # Instruction pointer

    def run(self):
        while self.ip < len(self.program):
            opcode = self.program[self.ip]

            if opcode == "PUSH":
                self.ip += 1
                value = self.program[self.ip]
                self.stack.append(value)

            elif opcode == "ASSIGN":
                variable_name = self.program[self.ip + 1]
                value = self.stack.pop()
                self.memory[variable_name] = value
                self.ip += 1
                
            elif opcode == "LOAD":
                variable_name = self.program[self.ip + 1]
                value = self.memory.get(variable_name)
                if value is not None:
                    self.stack.append(value)
                else:
                    raise ValueError(f"Variable '{variable_name}' not found.")
                self.ip += 1

            elif opcode == "SET":
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a)

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

            elif opcode == "EQL":
                a = self.stack.pop()
                b = self.stack.pop()
                if b == a:
                    self.stack.append(True)
                else:
                    self.stack.append(False)

            elif opcode == "NEQ":
                a = self.stack.pop()
                b = self.stack.pop()
                if b != a:
                    self.stack.append(True)
                else:
                    self.stack.append(False)
            
            elif opcode == "LSS":
                a = self.stack.pop()
                b = self.stack.pop()
                if b < a:
                    self.stack.append(True)
                else:
                    self.stack.append(False)

            elif opcode == "GTR":
                a = self.stack.pop()
                b = self.stack.pop()
                if b > a:
                    self.stack.append(True)
                else:
                    self.stack.append(False)

            elif opcode == "PRINT":
                variable_name = self.program[self.ip + 1]
                value = self.memory.get(variable_name)
                if value is not None:
                    print(value)
                else:
                    raise ValueError(f"Variable '{variable_name}' not found.")

            elif opcode == "START":
                self.stack.append(self.ip)

            elif opcode == "END":
                break

            elif opcode == "JUMP_IF_TRUE":
                jump_target = self.program[self.ip + 1]
                condition = self.stack.pop()
                if condition:
                    self.ip = jump_target
                else:
                    self.ip += 1

            self.ip += 1