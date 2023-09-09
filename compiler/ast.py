class Program:
    def __init__(self, cds, exprs):
        self.cds = cds
        self.exprs = exprs

class ASTNode:

    def __init__(self, node_type, identifier, value, children):
        self.node_type = node_type
        self.identifier = identifier
        self.value = value
        self.children = children if children is not None else []

    def add_child(self, parent, child):
        parent.children.append(child)

class AST_List:
    def __init__(self):
        self.list = []

    def add(self, ast):
        self.list.append(ast)

    def print_curr(self):
        for ast in self.list:
            self.print_ast(ast.root)

    def print_ast(self, node, indent=0):
        print("  " * indent + node.type, node.value)
        for child in node.children:
            self.print_ast(child, indent+1)

# Start = start
# Bool = true | false
# Number = [0-9] for all characters
# String = [a-zA-Z] for all characters
# Condition = Comparator -> Expression
# Comparator -> id | compOp | id
# Expression = id | op | id
# Update -> id | op | num/id
# End = end