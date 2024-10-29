import re 
from src.errors import LexicalError

# Definición de patrones de tokens
token_patterns = {
    'PRINT': r'^print',
    'LPAREN': r'^\(',
    'RPAREN': r'^\)',
    'STRING': r'^"[^"]*"'
}

def lex(code):
    tokens = []
    lines = code.splitlines()
    for line_num, line in enumerate(lines, start=1):
        while line:
            match_found = False
            # Intenta hacer coincidir los tokens válidos primero
            for token_name, pattern in token_patterns.items():
                match = re.match(pattern, line)
                if match:
                    match_found = True
                    tokens.append((token_name, match.group()))
                    line = line[match.end():].lstrip()  # Avanza solo después de un token válido
                    break
                
            # Si no se encontró un token válido, genera el error para el primer token inválido
            if not match_found:
                # Encuentra el primer token inválido sin consumir el resto de la línea
                invalid_token = re.match(r'^\w+', line).group()
                raise LexicalError(f"Error léxico en línea {line_num}: token '{invalid_token}' inválido.")
    return tokens
