from behave import given, when, then
from src.lexer import lex
from src.parser import parse
from src.executor import execute_code
from src.errors import LexicalError, SyntaxError

@given('el código fuente es')
def step_given_code(context):
    context.code = context.text

@when('el compilador ejecuta el código')
def step_when_execute(context):
    try:
        tokens = lex(context.code)
        parse(tokens)
        context.result = execute_code(tokens)
    except (LexicalError, SyntaxError) as e:
        context.result = str(e)

@then('el resultado debe ser')
def step_then_result(context):
    assert context.result.strip() == context.text.strip(), f"Resultado esperado: {context.text.strip()}, pero obtuvo: {context.result.strip()}"

