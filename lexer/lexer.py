import ply.lex as lex
from ply.lex import LexToken
from tokens_lexer import TOKENS, RESERVED

tokens = TOKENS

t_ignore = ' \t\n'

t_EQUALS         = r'='
t_NOT_EQUALS     = r'!='
t_GREATER_EQUALS = r'>='
t_LESS_EQUALS    = r'<='
t_GREATER        = r'>'
t_LESS           = r'<'
t_ASTERISK       = r'\*'
t_COMMA          = r','

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
    print(f"Błąd leksykalny: Nielegalny znak '{t.value[0]}' w linii {t.lineno}, pozycja {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()