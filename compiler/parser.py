import ast as AST
import re

# Define the grammar rules and mappings
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens

    validCharacters = {
    1: '\0',
    2: 'a',
    3: 'b',
    4: 'c',
    5: 'd',
    6: 'e',
    7: 'f',
    8: 'g',
    9: 'h',
    10: 'i',
    11: 'j',
    12: 'k',
    13: 'l',
    14: 'm',
    15: 'n',
    16: 'o',
    17: 'p',
    18: 'q',
    19: 'r',
    20: 's',
    21: 't',
    22: 'u',
    23: 'v',
    24: 'w',
    25: 'x',
    26: 'y',
    27: 'z',
    29: '0',
    30: '1',
    31: '2',
    32: '3',
    33: '4',
    34: '5',
    35: '6',
    36: '7',
    37: '8',
    38: '9',
    }

    expressions = {
        1: "start",
        2: "bool",
        3: "int",
        4: "string",
        5: "condition",
        6: "update",
        7: "end",
    }

    operators = {
        1: "=",
        2: "+",
        3: "-",
        4: "*",
        5: "/",
        6: "%",
    }

    conditionals = {
        1: "true",
        2: "false",
        3: "if",
        4: "and",
        5: "or",
    }

    comparators = {
        1: "=",
        2: ">",
        3: "<",
        4: "!=",
    }

    def parse_start(self):
        start = self.tokens.pop(0)
        if len(start != 1):
            raise Exception("Invalid start token")
        return self.create_node("start")
    
    def parse_end(self):
        end = self.tokens.pop(0)
        if len(end != 7):
            raise Exception("Invalid end token")
        return self.create_node("end")
    
    def determine_expression_type(self, tokens):
        expression = self.tokens.pop(0)
        expression_length = len(expression)

    def parse_expression(self):
        expression = self.tokens.pop(0)
        expression_length = len(expression)

        if expression_length not in self.expressions:
            raise Exception("Invalid rule token")

        if expression_length == 2:
            return self.parse_bool(expression)
        elif expression_length == 3:
            return self.parse_number(expression)
        elif expression_length == 4:
            return self.parse_string(expression)
        elif expression_length == 5:
            return self.parse_conditional(expression)
        elif expression_length == 6:
            return self.parse_update(expression)
        elif expression_length == 7:
            return self.parse_end(expression)
        else:
            raise Exception("Invalid expression token")

    def parse_bool(self, tokens):
        ident = self.parse_identifier(tokens)
        value = tokens.pop(0)
        if len(value != 1 and len(value != 2)):
            raise Exception("Invalid bool token")
        return AST.BoolNode(ident, value)

    def parse_conditional(self, tokens):
        comparator = self.parse_comparator(tokens)
        expression = self.parse_expression(tokens)
        return AST.ASTNode("conditional", None, None, [comparator, expression])

    def parse_update(self, tokens):
        identifier = self.parse_identifier(tokens)
        operator = tokens.pop(0)
        if not operator in self.operators.keys():
            raise Exception("Invalid operator token")
        identifier = self.parse_identifier(tokens)
        return AST.UpdateNode("update", None, None, [identifier, operator, identifier])

    def parse_comparator(self, tokens):
        leftVal = self.parse_identifier(tokens)
        if len(leftVal == 1):
            raise Exception("Invalid comparator token")
        
        comparator = tokens.pop(0)
        if not comparator in self.comparators.keys():
            raise Exception("Invalid comparator token")
        
        rightVal = self.parse_identifier(tokens)
        if len(rightVal == 1):
            raise Exception("Invalid comparator token")
        
        return AST.ComparatorNode("comparator", None, None, [leftVal, comparator, rightVal])

    def parse_expression(self, tokens):
        identifier = self.parse_identifier(tokens)
        if len(identifier == 1):
            raise Exception("Invalid expression token")
        
        operator = tokens.pop(0)
        if not operator in self.operators.keys():
            raise Exception("Invalid operator token")

        identifier = self.parse_identifier(tokens)
        if len(identifier == 1):
            raise Exception("Invalid expression token")
        
        return AST.ExpressionNode("expression", None, None, [identifier, operator, identifier])

    def parse_identifier(self, tokens):
        ident = ""
        while len(tokens) > 0:
            id = tokens.pop(0)
            if not id in self.validCharacters.keys():
                raise Exception("Invalid identifier token")
            if id == 1:
                break
            ident += self.validCharacters[id]
        if len(tokens) == 0 or ident == "":
            raise Exception("Invalid identifier token")
        return ident

    # Returns True if the identifier is a string
    def identifier_is_string(self, id):
        return re.search('[a-zA-Z]', id) is not None
    
    # Returns True if the identifier is a string
    def identifier_is_number(self, id):
        return re.search('[a-zA-Z]', id) is None
    
    # Parser function
    def parse_list(self, ast, tokens):
        # Create the root of the AST

        # Parse the tokens
        while len(tokens) > 1:
            new_expression = self.parse_rule(tokens)
            ast.add_child(ast.root, new_expression)
        return ast

    def create_program(self, tokens):
        consts = AST.AST_List()
        exprs = AST.AST_List()

        while len(tokens) > 0:
            expType = self.determine_expression_type(tokens)
            if expType == "const":
                consts.add(self.parse_expression(tokens))
            elif expType == "expr":
                exprs.add(self.parse_expression(tokens))
            else:
                raise Exception("Invalid expression type")
        
        
    
    # Print the AST (you can define a more elaborate printer function)
    def print_ast(self, node, indent=0):
        print("  " * indent + node.type, node.value)
        for child in node.children:
            self.print_ast(child, indent + 1)