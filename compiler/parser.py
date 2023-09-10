from compiler.ast import Program, AST, AST_List
import re

# Define the grammar rules and mappings
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    validCharacters = {
        1: "\0",
        2: "a",
        3: "b",
        4: "c",
        5: "d",
        6: "e",
        7: "f",
        8: "g",
        9: "h",
        10: "i",
        11: "j",
        12: "k",
        13: "l",
        14: "m",
        15: "n",
        16: "o",
        17: "p",
        18: "q",
        19: "r",
        20: "s",
        21: "t",
        22: "u",
        23: "v",
        24: "w",
        25: "x",
        26: "y",
        27: "z",
        29: "0",
        30: "1",
        31: "2",
        32: "3",
        33: "4",
        34: "5",
        35: "6",
        36: "7",
        37: "8",
        38: "9",
    }
    # declarations (reformat if time)
    expressions = {
        1: "start",
        2: "define",
        3: "condition",
        4: "update",
        5: "end",
    }

    datatypes = {
        1: "identifier",
        2: "bool",
        3: "int",
        4: "string",
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
        1: True,
        2: False,
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
        return AST("start", self.position, None, None, None, None)

    def parse_expression(self):
        expression = self.tokens.pop(0)
        expression_type= len(expression)

        if expression_type == 2:
            return self.parse_define()
        elif expression_type == 3:
            return self.parse_conditional()
        elif expression_type == 4:
            return self.parse_update()
        elif expression_type == 5:
            return AST("end", self.position, None, None, None, None)
        else:
            raise Exception("Invalid expression token")
        
    def parse_define(self):

        type = len(self.tokens.pop(0))
        if not type in self.datatypes.keys():
            raise Exception("Invalid type token")
        
        type = self.datatypes[type]
        defined_AST = None

        if type == "bool":
            defined_AST = self.parse_bool()
        elif type == "int":
            defined_AST = self.parse_number()
        elif type == "string":
            defined_AST = self.parse_string()
        else:
            raise Exception("Invalid type token")
        
        defined_AST.node_type = "define"
        return defined_AST

    # Parses a new bool for the ast
    def parse_bool(self):
        ident = self.parse_identifier()
        value = len(self.tokens.pop(0))
        if value != 1 and value != 2 or not value in self.conditionals.keys():
            raise Exception("Invalid bool parse token")
        value = self.conditionals[value]
        
        return AST(None, self.position, "bool", ident, value, None)

    # Parses a new number for the AST
    def parse_number(self):
        ident = self.parse_identifier()
        value = self.parse_identifier()

        if not self.value_is_number(value) or not self.value_is_string(ident):
            raise Exception("Invalid number parse token")

        return AST(None, self.position, "number", ident, int(value), None)
    
    def parse_string(self):
        ident = self.parse_identifier()
        value = self.parse_identifier()

        if not self.value_is_string(value) or not self.value_is_string(ident):
            raise Exception("Invalid string parse token")

        return AST(None, self.position, "string", ident, value, None)

    # Wrapper for a conditional
    def parse_conditional(self):
        comp = self.parse_comparator()
        expr = self.parse_expression()
        return AST("conditional", self.position, None, None, None, [comp, expr])
    
    # Example: a > 5
    def parse_comparator(self):
        
        leftType = len(self.tokens.pop(0))
        leftVal = self.parse_identifier()

        comparator = len(self.tokens.pop(0))
        if not comparator in self.comparators.keys():
            raise Exception("Invalid comparator token")

        rightType = len(self.tokens.pop(0))
        rightVal = self.parse_identifier()

        if not leftType in self.datatypes.keys() or not rightType in self.datatypes.keys():
            raise Exception("Invalid datatype token")

        leftType = self.datatypes[leftType]
        rightType = self.datatypes[rightType]

        if leftType == "bool" and leftVal <= 2 and leftVal in self.conditionals.keys():
            leftVal = self.conditionals[leftVal]
            leftVal = AST("conditional", self.position, "bool", None, leftVal, None)
        elif leftType == "int" and self.value_is_number(leftVal):
            leftVal = AST("conditional", self.position, "number", None, int(leftVal), None)
        elif leftType == "identifier" and self.value_is_string(leftVal):
            leftVal = AST("conditional", self.position, "identifier", leftVal, leftVal, None)
        elif leftType == "string" and self.value_is_string(leftVal):
            if not self.value_is_string(leftVal):
                raise Exception("Invalid left value token")
            leftVal = AST("conditional", self.position, "string", None, leftVal, None)
        else:
            raise Exception("Invalid left value token")
        
        if rightType == "bool" and rightVal <= 2 and rightVal in self.conditionals.keys():
            rightVal = self.conditionals[rightVal]
            rightVal = AST("conditional", self.position, "bool", None, rightVal, None)
        elif rightType == "int" and self.value_is_number(rightVal):
            rightVal = AST("conditional", self.position, "number", None, int(rightVal), None)
        elif rightType == "id" and self.value_is_string(rightVal):
            rightVal = AST("conditional", self.position, "identifier", rightVal, rightVal, None)
        elif rightType == "string" and self.value_is_string(rightVal):
            if not self.value_is_string(rightVal):
                raise Exception("Invalid right value token")
            rightVal = AST("conditional", self.position, "string", None, rightVal, None)
        else:
            raise Exception("Invalid right value token")
            
        return AST(
            "comparator", self.position, None, None, None, [leftVal, comparator, rightVal]
        )

    # Example: a + 1
    def parse_update(self):

        id1 = self.parse_identifier()
        if not self.value_is_string(id1):
            raise Exception("Invalid update token")
        
        operator = len(self.tokens.pop(0))
        if not operator in self.operators.keys():
            raise Exception("Invalid operator token")
        
        id2 = self.parse_identifier()

        return AST("update", self.position, None, None, None, [id1, operator, id2])

    def parse_identifier(self):
        ident = ""

        while len(self.tokens) > 0:
            id = len(self.tokens.pop(0))
            if not id in self.validCharacters.keys():
                raise Exception("Invalid identifier token")
            if id == 1:
                break
            ident += self.validCharacters[id]

        if len(self.tokens) == 0 or ident == "":
            raise Exception("Invalid identifier token")

        return ident

    # Returns True if the identifier is a string
    def value_is_string(self, val):
        return val[0].isalpha()

    # Returns True if the identifier is a number
    def value_is_number(self, val):
        return re.search("[a-zA-Z]", val) is None
    
    # TODO
    def value_is_bool(self, val):
        pass

    # Parser function
    def create_program(self):
        exprs = AST_List()

        startExpr = self.parse_start()
        if startExpr.node_type != "start":
            raise Exception("Invalid start type")
        exprs.add(startExpr)

        self.position += 1

        while len(self.tokens) != 0:
            exprs.add(self.parse_expression())
            print(exprs.list[-1])
            print(self.tokens)
            self.position += 1
            if exprs.list[-1].node_type == "end":
                break

        # This should not run if code format is correct
        if len(self.tokens) != 0 or exprs.list[-1].node_type != "end":
            raise Exception("Invalid end or program type")

        return Program(exprs)