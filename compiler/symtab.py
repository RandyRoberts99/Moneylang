class SymbolTable:
    def __init__(self):
        self._symbols = {}

    def add(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        return self._symbols.get(name)

    def __str__(self):
        return 'Symbols: {0}'.format([value for value in self._symbols.values()])