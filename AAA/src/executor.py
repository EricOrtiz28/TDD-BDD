def execute_code(tokens):
    command = tokens[0][0]
    if command == 'PRINT':
        string_value = tokens[2][1]  # Extraer el valor de la cadena
        return string_value.strip('"')
