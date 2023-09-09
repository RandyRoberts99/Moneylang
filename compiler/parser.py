from compiler.ast import Program, AST, AST_List
import re

# Define the grammar rules and mappings
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

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
        if len(start) != 1:
            raise Exception("Invalid start token")
        return AST("start", self.position, None, None, None)
    
    def parse_end(self):
        end = self.tokens.pop(0)
        if len(end) != 7:
            raise Exception("Invalid end token")
        return AST("end", self.position, None, None, None)
    
    def determine_expression_type(self):
        expression = self.tokens[0]
        expression_length = len(expression)

        if expression_length >= 2 and expression_length <= 4:
            return "const"
        elif expression_length >= 5 and expression_length <= 6:
            return "expr"
        elif expression_length == 7:
            return "end"
        else:
            raise Exception("Invalid expression token")

    def parse_expression(self):
        expression = self.tokens.pop(0)
        expression_length = len(expression)

        if expression_length not in self.expressions:
            raise Exception("Invalid rule token")

        if expression_length == 2:
            return self.parse_bool()
        elif expression_length == 3:
            return self.parse_number()
        elif expression_length == 4:
            return self.parse_string()
        elif expression_length == 5:
            return self.parse_conditional()
        elif expression_length == 6:
            return self.parse_update()
        elif expression_length == 7:
            return self.parse_end()
        else:
            raise Exception("Invalid expression token")

    def parse_bool(self):
        ident = self.parse_identifier()
        print(f'ident: {ident}')
        value = self.tokens.pop(0)
        value = len(value)
        print(f'value: {value}')
        if value != 1 and value != 2:
            raise Exception("Invalid bool token")
        return AST("bool", self.position, ident, value, None)

    def parse_number(self):

        ident = self.parse_identifier()
        value = self.parse_identifier()

        if not self.identifier_is_number(value) or not self.identifier_is_string(ident):
            raise Exception("Invalid number parse token")
        
        return AST("number", self.position, ident, value)

    def parse_conditional(self):
        comparator = self.parse_comparator()
        expression = self.parse_expression()
        return AST("conditional", self.position, None, None, [comparator, expression])

    def parse_update(self):
        identifier = self.parse_identifier()
        operator = self.tokens.pop(0)
        if not operator in self.operators.keys():
            raise Exception("Invalid operator token")
        identifier = self.parse_identifier()
        return AST("update", self.position, None, None, [identifier, operator, identifier])

    def parse_comparator(self):
        leftVal = self.parse_identifier()
        if len(leftVal == 1):
            raise Exception("Invalid comparator token")
        
        comparator = self.tokens.pop(0)
        if not comparator in self.comparators.keys():
            raise Exception("Invalid comparator token")
        
        rightVal = self.parse_identifier()
        if len(rightVal == 1):
            raise Exception("Invalid comparator token")
        
        return AST("comparator", self.position, None, None, [leftVal, comparator, rightVal])

    def parse_identifier(self):

        ident = ""

        while len(self.tokens) > 0:
            id = self.tokens.pop(0)
            id = len(id)
            if not id in self.validCharacters.keys():
                raise Exception("Invalid identifier token")
            if id == 1:
                break
            ident += self.validCharacters[id]

        if len(self.tokens) == 0 or ident == "":
            raise Exception("Invalid identifier token")
        
        return ident

    # Returns True if the identifier is a string
    def identifier_is_string(id):
        return re.search('[a-zA-Z]', id) is not None
    
    # Returns True if the identifier is a number
    def identifier_is_number(id):
        return re.search('[a-zA-Z]', id) is None
    
    # Parser function
    def create_program(self):
        
        consts = AST_List()
        exprs = AST_List()

        startExpr = self.parse_start()
        if startExpr.node_type != "start":
            raise Exception("Invalid start type")
        exprs.add(startExpr)

        self.position += 1

        while len(self.tokens) != 0 and self.determine_expression_type() != "end":
            expType = self.determine_expression_type()
            if expType == "const":
                consts.add(self.parse_expression())
            elif expType == "expr":
                exprs.add(self.parse_expression())
            else:
                raise Exception("Invalid expression type")
            self.position += 1
        
        exprs.add(self.parse_end())
        if len(self.tokens) != 0 or exprs.list[-1].node_type != "end":
            raise Exception("Invalid end type")
        
        return Program(consts, exprs)