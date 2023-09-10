import re

class Code_Gen:
    
    def __init__(self, program):
        self.program = program
        self.code_seq = []

    def generate_code(self):
        exprs = self.program.exprs.list
        while len(exprs) != 0:
            self.generate_code_seq(exprs.pop(0))

        return self.code_seq

    def generate_code_seq(self, ir):

        if ir.node_type == "start":
            self.generate_start_seq(ir)

        elif ir.node_type == "define":
            self.generate_bool_seq(ir)

        elif ir.node_type == "contitional":
            self.generate_number_seq(ir)

        elif ir.node_type == "update":
            self.generate_string_seq(ir)

        elif ir.node_type == "end":
            self.generate_condition_seq(ir)

        else:
            raise Exception("Invalid node type")

    def generate_start_seq(self, ir):
        self.code_seq.append("START")

    def generate_end_seq(self, ir):
        self.code_seq.append("END")

    def generate_bool_seq(self, ir):
        self.code_seq.append("PUSH")

        if ir.value == 1:
            self.code_seq.append("True")
        elif ir.value == 2:
            self.code_seq.append("False")
        else:
            raise Exception("Invalid bool value")

        self.code_seq.append("ASSIGN")
        self.code_seq.append(ir.identifier)

    def generate_number_seq(self, ir):
        self.generate_push_seq(ir)
        self.generate_assign_seq(ir)

    def generate_string_seq(self, ir):
        self.generate_push_seq(ir)
        self.generate_assign_seq(ir)

    def generate_update_seq(self, ir):

        if self.identifier_is_string(ir.children[0]):
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[0])
        else:
            raise Exception("Invalid Statement")

        if self.identifier_is_string(ir.children[2]):
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[2])
        else:
            self.code_seq.append("PUSH")
            self.code_seq.append(ir.children[2])

        self.generate_op_seq(ir.children[1])
        self.code_seq.append("ASSIGN")
        
        self.code_seq.append(ir.children[0])

    def generate_condition_seq(self, ir):
        self.generate_comparator_seq(ir.children[0])

        self.code_seq.append("JUMP_IF_TRUE")  # Jump if the condition is true
        jump_target = len(self.code_seq) + 2
        self.code_seq.append(jump_target)  # Jump target label

        self.generate_expr_seq(ir.children[1])

    def generate_comparator_seq(self, ir):

        if self.identifier_is_string(ir.children[0]):
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[0])
        else:
            self.code_seq.append("PUSH")
            self.code_seq.append(ir.children[0])

        if self.identifier_is_string(ir.children[2]):
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[2])
        else:
            self.code_seq.append("PUSH")
            self.code_seq.append(ir.children[2])

        self.generate_relOp_seq(ir.children[1])

    def generate_expr_seq(self, ir):
        if ir.node_type == "conditional":
            self.generate_condition_seq(ir)
        elif ir.node_type == "update":
            self.generate_update_seq(ir)
        else:
            raise Exception("Invalid expression type")

    def generate_relOp_seq(self, op):
        if op == 1:
            self.code_seq.append("EQU")
        elif op == 2:
            self.code_seq.append("GTR")
        elif op == 3:
            self.code_seq.append("LSS")
        elif op == 4:
            self.code_seq.append("NEQ")
        else:
            raise Exception("Invalid compOp value")

    def generate_op_seq(self, op):
        if op == 1:
            self.code_seq.append("SET")
        elif op == 2:
            self.code_seq.append("ADD")
        elif op == 3:
            self.code_seq.append("SUB")
        elif op == 4:
            self.code_seq.append("MUL")
        elif op == 5:
            self.code_seq.append("DIV")
        elif op == 6:
            self.code_seq.append("MOD")
        else:
            raise Exception("Invalid op value")
        
    def generate_push_seq(self, ir):
        self.code_seq.append("PUSH")
        self.code_seq.append(ir.value)

    def generate_assign_seq(self, ir):
        self.code_seq.append("ASSIGN")
        self.code_seq.append(ir.identifier)

    # Returns True if the identifier is a string
    def identifier_is_string(self, id):
        return id[0].isalpha()

    # Returns True if the identifier is a number
    def identifier_is_number(self, id):
        return re.search("[a-zA-Z]", id) is None