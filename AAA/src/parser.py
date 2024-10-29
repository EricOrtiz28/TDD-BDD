from src.errors import SyntaxError

def parse(tokens):
    if not tokens:
        raise SyntaxError("Error sintáctico: código vacío.")
    
    # Reglas para la gramática básica
    expected_tokens = ['PRINT', 'LPAREN', 'STRING', 'RPAREN']
    token_types = [token[0] for token in tokens]
    
    if token_types != expected_tokens:
        if 'LPAREN' not in token_types or 'RPAREN' not in token_types:
            raise SyntaxError("Error sintáctico en línea 1: paréntesis faltante.")
        raise SyntaxError("Error sintáctico: se esperaba 'print(\"string\")'.")
