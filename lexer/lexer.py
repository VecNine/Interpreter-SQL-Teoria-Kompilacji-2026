import ply.lex as lex
from ply.lex import LexToken

from errors.errors import SqlSyntaxError
from lexer.tokens_lexer import TOKENS, RESERVED

tokens = TOKENS

t_ignore = ' \t'

t_EQUALS         = r'='
t_NOT_EQUALS     = r'!='
t_GREATER_EQUALS = r'>='
t_LESS_EQUALS    = r'<='
t_GREATER        = r'>'
t_LESS           = r'<'
t_ASTERISK       = r'\*'
t_COMMA          = r','
t_SEMICOLON      = r';'
t_LPAREN         = r'\('
t_RPAREN         = r'\)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_FLOAT(t) -> LexToken:
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t) -> LexToken:
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t) -> LexToken:
    r'("[^"]*")|(\'[^\']*\')'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t) -> LexToken:
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = RESERVED.get(t.value.lower(), 'IDENTIFIER')
    return t

def t_error(t) -> None:
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    column = (t.lexpos - line_start) + 1

    raise SqlSyntaxError(
        f"Błąd leksykalny w linii {t.lineno}, kolumnie {column}: "
        f"Nielegalny znak '{t.value[0]}'"
    )

lexer = lex.lex()