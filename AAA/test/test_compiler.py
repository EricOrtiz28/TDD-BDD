import pytest 
import sys
import os

# Modifica sys.path antes de las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import lex
from src.parser import parse
from src.executor import execute_code
from src.errors import LexicalError, SyntaxError

def test_compilacion_exitosa():
    # Arrange
    code = 'print("Hello, World!")'
    # Act
    tokens = lex(code)
    parse(tokens)
    result = execute_code(tokens)
    # Assert
    assert result == "Hello, World!"

def test_error_lexico():
    code = 'prnt("Hello, World!")'
    with pytest.raises(LexicalError):
        tokens = lex(code)

def test_error_sintactico():
    code = 'print "Hello, World!"'
    tokens = lex(code)
    with pytest.raises(SyntaxError):
        parse(tokens)
