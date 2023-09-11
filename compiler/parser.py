from compiler.ast import Program, AST, AST_List
import re

# Define the grammar rules and mappings
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.symbols = {}

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
        5: "print",
        5: "end",
    }

    datatypes = {
        1: "identifier",
        2: "bool",
        3: "number",
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
        1: "==",
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
            return self.parse_print()
        elif expression_type == 6:
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
        elif type == "number":
            defined_AST = self.parse_number()
        elif type == "string":
            defined_AST = self.parse_string()
        else:
            raise Exception("Invalid type token")
        
        # Pre-made symbol table for type checking
        self.symbols[defined_AST.identifier] = defined_AST.datatype

        defined_AST.node_type = "define"
        return defined_AST

    # Parses a new bool for the ast
    def parse_bool(self):
        ident = self.parse_keyword()
        value = len(self.tokens.pop(0))
        if not (value <= 2 and value in self.conditionals.keys()):
            raise Exception("Invalid bool parse token")
        value = self.conditionals[value]
        
        return AST(None, self.position, "bool", ident, value, None)

    # Parses a new number for the AST
    def parse_number(self):
        ident = self.parse_keyword()
        value = self.parse_keyword()

        if not self.value_is_number(value) or not self.value_is_string(ident):
            raise Exception("Invalid number parse token")

        return AST(None, self.position, "number", ident, int(value), None)
    
    def parse_string(self):
        ident = self.parse_keyword()
        value = self.parse_keyword()

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
        leftVal = self.parse_keyword()

        comparator = len(self.tokens.pop(0))
        if not comparator in self.comparators.keys():
            raise Exception("Invalid comparator token")
        comparator = AST("comparator", self.position, None, None, comparator, None)

        rightType = len(self.tokens.pop(0))
        rightVal = self.parse_keyword()

        if not leftType in self.datatypes.keys() or not rightType in self.datatypes.keys():
            raise Exception("Invalid datatype token")

        leftType = self.datatypes[leftType]
        rightType = self.datatypes[rightType]

        if leftType == "bool" and leftVal <= 2 and leftVal in self.conditionals.keys():
            leftVal = self.conditionals[leftVal]
            leftVal = AST("conditional", self.position, "bool", None, leftVal, None)
        elif leftType == "number" and self.value_is_number(leftVal):
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
        elif rightType == "number" and self.value_is_number(rightVal):
            rightVal = AST("conditional", self.position, "number", None, int(rightVal), None)
        elif rightType == "identifier" and self.value_is_string(rightVal):
            rightVal = AST("conditional", self.position, "identifier", rightVal, rightVal, None)
        elif rightType == "string" and self.value_is_string(rightVal):
            if not self.value_is_string(rightVal):
                raise Exception("Invalid right value token")
            rightVal = AST("conditional", self.position, "string", None, rightVal, None)
        else:
            raise Exception("Invalid right value token")
        
        # Perform leftType and rightType checks
        if leftType == "identifier" and leftVal.value in self.symbols.keys():
            if self.symbols[leftVal.value] != rightType:
                raise Exception("Invalid type match token in comparator. Cannot compare types.") 
            
        if rightType == "identifier" and rightVal.value in self.symbols.keys():
            if self.symbols[rightVal.value] != leftType:
                raise Exception("Invalid type match token in comparator. Cannot compare types.")
        
        # Check raw-types (String vs String, Int vs Int, etc.)
        if leftType != rightType and leftType != "identifier" and rightType != "identifier":
            raise Exception("Invalid type match token in comparator. Cannot compare types.")

        return AST(
            "comparator", self.position, None, None, None, [leftVal, comparator, rightVal]
        )

    # Example: <id><relop><type><value> or a + (int) 1
    def parse_update(self):

        id1Value = self.parse_keyword()
        if not self.value_is_string(id1Value) or not id1Value in self.symbols.keys():
            raise Exception("Invalid left id token in update")
        
        operator = len(self.tokens.pop(0))
        if not operator in self.operators.keys():
            raise Exception("Invalid operator token in update")

        id2Type = len(self.tokens.pop(0))
        if not id2Type in self.datatypes.keys():
            raise Exception("Invalid right type token in update")
        id2Type = self.datatypes[id2Type]

        id2Value = self.parse_keyword()

        if id2Type == "bool":
            id2 = len(id2)
            if not (id2 <= 2 and id2 in self.conditionals.keys()):
                raise Exception("Invalid bool token in update")
            id2Value = self.conditionals[id2Value]
        elif id2Type == "number":
            if not self.value_is_number(id2Value):
                raise Exception("Invalid number token in update")
            id2Value = int(id2Value)
        elif id2Type == "string":
            if not self.value_is_string(id2Value):
                raise Exception("Invalid string token in update")
        elif id2Type == "identifier":
            if not self.value_is_string(id2Value) or not id2Value in self.symbols.keys():
                raise Exception("Invalid identifier token in update")
            if not (self.symbols[id2Value] == self.symbols[id1Value]):
                raise Exception("Invalid type match token in update")
        else:
            raise Exception("Invalid right type token in update")

        return AST("update", self.position, None, None, None, [id1Value, operator, id2Type, id2Value])

    def parse_print(self):

        pType = self.datatypes[len(self.tokens.pop(0))]

        if pType == "identifier":
            pValue = self.parse_keyword()
            if not self.value_is_string(pValue) or not pValue in self.symbols.keys():
                raise Exception("Invalid identifier token in print")
            return AST("print", self.position, None, pType, pValue, None)
        
        elif pType == "bool":
            pValue = len(self.tokens.pop(0))
            if pValue != 1 and pValue != 2:
                raise Exception("Invalid bool token in update")
            pValue = self.conditionals[pValue]
            return AST("print", self.position, None, pType, pValue, None)
        
        elif pType == "string":
            pValue = self.parse_keyword()
            if not self.value_is_string(pValue):
                raise Exception("Invalid string token in print")
            return AST("print", self.position, None, pType, pValue, None)
        
        elif pType == "number":
            pValue = self.parse_keyword()
            if not self.value_is_number(pValue):
                raise Exception("Invalid number token in print")
            return AST("print", self.position, None, pType, int(pValue), None)
        else:
            raise Exception("Invalid print token")
        
    def parse_keyword(self):
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

    # Returns True if the value is an identifier or string
    def value_is_string(self, val):
        return val[0].isalpha()

    # Returns True if the identifier is a number
    def value_is_number(self, val):
        return re.search("[a-zA-Z]", val) is None

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
            self.position += 1
            if exprs.list[-1].node_type == "end":
                break

        # This should not run if code format is correct
        if len(self.tokens) != 0 or exprs.list[-1].node_type != "end":
            raise Exception("Invalid end or program type")
        
        return Program(exprs)