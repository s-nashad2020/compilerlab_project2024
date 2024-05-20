# Importing necessary libraries
import re
import gradio as gr

# Defining token patterns for lexical analysis
TOKEN_PATTERNS = {
    'IF': r'if',
    'THEN': r'then',
    'ELSE': r'else',
    'IDENTIFIER': r'[a-zA-Z_]\w*',
    'NUMBER': r'\d+(\.\d+)?',
    'OPERATOR': r'[+\-*/]',
    'PAREN': r'[()]',
    'COMPARE_OP': r'[<>!=]=?|>=?|<=?',
    'WHITESPACE': r'\s+',
    'COMMENT': r'#.*',
}

# Function to tokenize the input string
def lexer(input_string):
    tokens = []
    index = 0
    print("Input: ", input_string)

    while index < len(input_string):
        match = None
        for token_name, token_pattern in TOKEN_PATTERNS.items():
            regex = re.compile(token_pattern)
            match = regex.match(input_string, index)
            if match:
                value = match.group()
                if token_name not in ['WHITESPACE', 'COMMENT']:
                    tokens.append((token_name, value))
                index = match.end()
                break

        if not match:
            raise ValueError(f"Unexpected token at index {index}: {input_string[index]}")

        print("Tokens collected: ", tokens)

    return tokens

# Parser class to handle tokenized input
class SyntaxParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if self.tokens else None

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def parse_condition(self):
        left_expr = self.parse_expression()
        if self.current_token and self.current_token[0] == 'COMPARE_OP':
            operator = self.current_token[1]
            self.advance()
            right_expr = self.parse_expression()
            operator = '==' if operator == '=' else operator
            return f"{left_expr} {operator} {right_expr}"
        elif self.current_token and self.current_token[0] == 'THEN':
            return left_expr
        else:
            raise ValueError("Condition parsing error")

    def parse_factor(self):
        if self.current_token[0] == 'NUMBER':
            value = float(self.current_token[1])
            self.advance()
            return value
        elif self.current_token[0] == 'PAREN' and self.current_token[1] == '(':
            self.advance()
            result = self.parse_expression()
            if self.current_token and self.current_token[0] == 'PAREN' and self.current_token[1] == ')':
                self.advance()
                return result
            else:
                raise ValueError("Mismatched parentheses")
        elif self.current_token[0] == 'IF':
            self.advance()
            condition = self.parse_condition()
            if self.current_token and self.current_token[0] == 'THEN':
                self.advance()
                then_branch = self.parse_expression()
                if self.current_token and self.current_token[0] == 'ELSE':
                    self.advance()
                    else_branch = self.parse_expression()
                    return then_branch if eval(condition) else else_branch
                else:
                    raise ValueError("Missing 'else' in conditional")
            else:
                raise ValueError("Missing 'then' in conditional")
        elif self.current_token[0] == 'IDENTIFIER':
            self.advance()
            return self.current_token[1]
        else:
            raise ValueError("Invalid factor")

    def parse_term(self):
        result = self.parse_factor()
        while self.current_token and self.current_token[1] in ('*', '/'):
            operator = self.current_token[1]
            self.advance()
            value = self.parse_factor()
            result = result * value if operator == '*' else result / value
        print("Term result: ", result)
        return result

    def parse_expression(self):
        result = self.parse_term()
        while self.current_token and self.current_token[1] in ('+', '-'):
            operator = self.current_token[1]
            self.advance()
            value = self.parse_term()
            result = result + value if operator == '+' else result - value
        print("Expression result: ", result)
        return result

# Function to evaluate an input expression
def evaluate(input_expr):
    try:
        tokens = lexer(input_expr)
        parser = SyntaxParser(tokens)
        result = parser.parse_expression()
        return f"Result: {result}"
    except Exception as error:
        return f"Error: {str(error)}"

# New sample input expression for testing
sample_input = 'if 3>2 then 10*2 else 20/2'
print(evaluate(sample_input))

# Creating Gradio interface for user interaction
interface = gr.Interface(
    fn=evaluate,
    inputs=gr.Textbox(label="Enter an expression:"),
    outputs="text",
    title="Expression Evaluator"
)

interface.launch()
