import re


class Code_Gen:
    def __init__(self, program):
        self.program = program
        self.code_seq = []

    def generate_code(self):
        exprs = self.program.exprs.list
        while len(exprs) != 0:
            self.generate_cmd(exprs.pop(0))

        return self.code_seq

    def generate_cmd(self, ir):
        if ir.node_type == "start":
            self.generate_start(ir)

        elif ir.node_type == "define":
            self.generate_define(ir)

        elif ir.node_type == "conditional":
            self.generate_conditional(ir)

        elif ir.node_type == "update":
            self.generate_update(ir)

        elif ir.node_type == "end":
            self.generate_end(ir)

        else:
            raise Exception("Invalid node type")

    def generate_start(self, ir):
        self.code_seq.append("START")

    def generate_end(self, ir):
        self.code_seq.append("END")

    def generate_define(self, ir):
        self.generate_push(ir)
        self.generate_assign(ir)

    # [id1, operator, id2Type, id2]
    def generate_update(self, ir):

        # This will always be an identifier
        self.code_seq.append("LOAD")
        self.code_seq.append(ir.children[0])

        if ir.children[2] == "identifier":
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[2])
        else:
            self.code_seq.append("PUSH")
            self.code_seq.append(ir.children[3])

        self.generate_op(ir.children[1])
        self.code_seq.append("ASSIGN")
        self.code_seq.append(ir.children[0])

    def generate_conditional(self, ir):
        self.generate_comparator(ir.children[0])

        self.code_seq.append("JUMP")
        jump_target = ir.position + 5
        self.code_seq.append(jump_target)

        self.generate_expr(ir.children[1])

    def generate_comparator(self, ir):
        if ir.children[0].datatype == "identifier":
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[0].value)
        else:
            self.code_seq.append("PUSH")
            self.code_seq.append(ir.children[0].value)

        if ir.children[2].datatype == "identifier":
            self.code_seq.append("LOAD")
            self.code_seq.append(ir.children[2].value)
        else:
            self.code_seq.append("PUSH")
            self.code_seq.append(ir.children[2].value)

        self.generate_relOp(ir.children[1].value)

    def generate_expr(self, ir):
        if ir.node_type == "conditional":
            self.generate_condition(ir)
        elif ir.node_type == "update":
            self.generate_update(ir)
        else:
            raise Exception("Invalid expression type")

    def generate_relOp(self, op):
        if op == 1:
            self.code_seq.append("EQL")
        elif op == 2:
            self.code_seq.append("GTR")
        elif op == 3:
            self.code_seq.append("LSS")
        elif op == 4:
            self.code_seq.append("NEQ")
        else:
            raise Exception("Invalid relOp value")

    def generate_op(self, op):
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

    def generate_push(self, ir):
        self.code_seq.append("PUSH")
        self.code_seq.append(ir.value)

    def generate_assign(self, ir):
        self.code_seq.append("ASSIGN")
        self.code_seq.append(ir.identifier)

    # Returns True if the identifier is a string or identifier
    def value_is_string(self, id):
        return id[0].isalpha()

    # Returns True if the identifier is a number
    def value_is_number(self, id):
        return re.search("[a-zA-Z]", id) is None
