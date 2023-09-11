# About Moneylang:

### Money talks. That is all. (no jk)

## Moneylang is designed to use only two characters - '💰', and ' '.
Parsing is extremely contextual, and requires an
understanding of the rules of the language.

## Each expression must start with a command. Commands can be found below:
1. Start - Starts the program syntax
2. End - Ends the program syntax
3. Define - Creates a new variable in the format (define)(type)(id)(value).
4. Update - Updates a value in the program in the format (id)(op)(val) 
5. Conditional - A basic if-statement. You can have nested if-statements. Format is(comparator)(expr)

## Keys:
1. (type) = The specified type of the variable.
2. (id) = The name of the variable.
3. (value) = The value of that variable relative to the type. (For example: strings and references can be interchanged)
4. (op) = Any valid computational operator. (=,+,-,*,/,%)
5. (comparator) = A comparison statement. (a ) b)
6. (expr) An expression. It could be a Define, Update, or Conditional statement.

### Moneybags are grouped together and seperated by spaces. 
### A basic program that starts and ends can be defined by: '💰 💰💰💰💰💰💰'