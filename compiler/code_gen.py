from compiler.ast import Program, AST, AST_List

class Code_Gen:
    def __init__(self, program):
        self.program = program
        self.code_seq = []

    def generate_code(self):

        cds = self.program.cds.list
        exprs = self.program.exprs.list

        while len(cds) > 0 and len(exprs) > 0:
            if cds[0].position < exprs[0].position:
                self.generate_code_seq(cds.pop(0))
            else:
                self.generate_code_seq(exprs.pop(0))

        while len(cds) != 0:
            self.generate_code_seq(cds.pop(0))
        while len(exprs) != 0:
            self.generate_code_seq(exprs.pop(0))

        self.code_seq.append("HALT")

    def generate_code_seq(self, ir):

        if ir.node_type == "start":
            self.generate_start_seq(ir)

        elif ir.node_type == "bool":
            self.generate_bool_seq(ir)

        elif ir.node_type == "int":
            self.generate_int_seq(ir)

        elif ir.node_type == "string":
            self.generate_string_seq(ir)

        elif ir.node_type == "condition":
            self.generate_condition_seq(ir)

        elif ir.node_type == "update":
            self.generate_update_seq(ir)

        elif ir.node_type == "end":
            self.generate_end_seq(ir)

        else:
            raise Exception("Invalid node type")
        
    def generate_start_seq(self, ir):
        self.code_seq.append("START")

    def generate_end_seq(self, ir):
        self.code_seq.append("END")

    def generate_bool_seq(self, ir):

        self.code_seq.append("PUSH")

        if ir.value == "1":
            self.code_seq.append("True")
        else:
            self.code_seq.append("False")

        self.code_seq.append("ASSIGN")
        self.code_seq.append(ir.identifier)

    def generate_int_seq(self, ir):
        self.code_seq.append("PUSH")
        self.code_seq.append(ir.value)
        self.code_seq.append("ASSIGN")
        self.code_seq.append(ir.identifier)

    def generate_string_seq(self, ir):
        self.code_seq.append("PUSH")
        self.code_seq.append(ir.value)

    def generate_condition_seq(self, ir):
        # Assuming ir has attributes condition_expr and jump_target
        self.generate_code_seq(ir.condition_expr)
        self.code_seq.append("JUMP_IF_TRUE")  # Jump if the condition is true
        self.code_seq.append(ir.jump_target)  # Jump target label

    def generate_update_seq(self, ir):
        # Assuming ir has attributes variable_name and new_value
        self.code_seq.append("PUSH")
        self.code_seq.append(ir.new_value)  # Push the new value onto the stack
        self.code_seq.append("ASSIGN")      # Assign the new value to the variable
        self.code_seq.append(ir.variable_name)

    def append_to_code_seq(self, code):
        self.code_seq.append(code)
