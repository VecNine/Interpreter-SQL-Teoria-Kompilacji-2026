import ply.yacc as yacc
from lexer.lexer import tokens
from lexer.lexer import lexer

precedence : tuple[tuple[str, str], tuple[str, str]] = (
    ('left', 'OR'),
    ('left', 'AND'),
)

def p_query(p) -> None:
    '''query : SELECT column_list FROM STRING where_clause order_clause limit_clause'''
    p[0] = {
        'select': p[2],
        'from': p[4],
        'where': p[5],
        'order': p[6],
        'limit': p[7]
    }

# =======================================
#          REGUŁY DLA SELECT
# =======================================

def p_column_list_asterisk(p) -> None:
    '''column_list : ASTERISK'''
    p[0] = '*'

def p_column_list_single(p) -> None:
    '''column_list : IDENTIFIER'''
    p[0] = [p[1]]

def p_column_list_multiple(p) -> None:
    '''column_list : column_list COMMA IDENTIFIER'''
    p[1].append(p[3])
    p[0] = p[1]




# =======================================
#          REGUŁY DLA WHERE
# =======================================

def p_where_clause_empty(p) -> None:
    '''where_clause : empty'''
    p[0] = None

def p_where_clause(p) -> None:
    '''where_clause : WHERE condition'''
    p[0] = p[2]

def p_condition_logic(p) -> None:
    '''condition : condition AND condition
                 | condition OR condition'''
    p[0] = ('LOGIC', p[2].upper(), p[1], p[3])

def p_condition_relation(p) -> None:
    '''condition : IDENTIFIER operator value'''
    p[0] = ('RELATION', p[2], p[1], p[3])

def p_operator(p) -> None:
    '''operator : EQUALS
                | NOT_EQUALS
                | GREATER
                | LESS
                | GREATER_EQUALS
                | LESS_EQUALS'''
    p[0] = p[1]

def p_value(p) -> None:
    '''value : INTEGER
             | FLOAT
             | STRING'''
    p[0] = p[1]



# =======================================
#        REGUŁY DLA ORDER BY
# =======================================

def p_order_clause_empty(p) -> None:
    '''order_clause : empty'''
    p[0] = None

def p_order_clause(p) -> None:
    '''order_clause : ORDER BY IDENTIFIER ASC
                    | ORDER BY IDENTIFIER DESC'''
    p[0] = (p[3], p[4].upper())





# =======================================
#        REGUŁY DLA LIMIT
# =======================================


def p_limit_clause_empty(p) -> None:
    '''limit_clause : empty'''
    p[0] = None

def p_limit_clause(p) -> None:
    '''limit_clause : LIMIT INTEGER'''
    p[0] = p[2]



# =======================================
#        REGUŁY DLA POMOCNICZE
# =======================================


def p_empty(p) -> None:
    '''empty :'''
    pass

def p_error(p) -> None:
    if p:
        print(f"Błąd składniowy w pobliżu tokena '{p.value}' (Typ: {p.type}, Linia: {p.lineno})")
    else:
        print("Błąd składniowy na końcu pliku (niekompletne zapytanie).")


parser = yacc.yacc()