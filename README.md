we are creating a CFG for simple arithmetic expressions involving addition and multiplication, with parentheses allowed. Here's the CFG:

1. S -> E
2. E -> E + T | T
3. T -> T * F | F
4. F -> (E) | num

In this CFG:
S is the start symbol.
E represents an expression.
T represents a term.
F represents a factor.
'num' represents a numerical value.
'+' represents addition.
'*' represents multiplication.
'(' and ')' represent parentheses.
