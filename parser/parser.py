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

def p_query_drop_table(p) -> None:
    '''query: DROP TABLE IDENTIFIER'''
    p[0] = {
        'action': 'DROP TABLE',
        'table_name': p[3]
    }

def p_query_create_table(p) -> None:
    '''query : CREATE TABLE IDENTIFIER LPAREN column_list_def_create RPAREN'''
    p[0] = {
        'action': 'CREATE TABLE',
        'table_name': p[3],
        'columns': p[5]
    }

def p_query_insert_table(p) -> None:
    '''query: INSERT INTO INDENTIFIER LPAREN column_list_def_insert RPAREN'''


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
#          REGUŁY POMOCNICZE
# =======================================


def p_empty(p) -> None:
    '''empty :'''
    pass

def p_error(p) -> None:
    if p:
        print(f"Błąd składniowy w pobliżu tokena '{p.value}' (Typ: {p.type}, Linia: {p.lineno})")
    else:
        print("Błąd składniowy na końcu pliku (niekompletne zapytanie).")



# =======================================
#           REGUŁY CREATE
# =======================================

# ====== POJEDYNCZE ELEMENTY ============

def p_column_def_create_varchar(p) -> None:
    '''column_def_create : IDENTIFIER VARCHAR LPAREN INTEGER RPAREN'''
    p[0] = {
        'identifier': p[1],
        'type': 'VARCHAR',
        'length': p[4]
    }

def p_column_def_create_numeric(p) -> None:
    '''column_def_create : IDENTIFIER NUMERIC LPAREN INTEGER COMMA INTEGER RPAREN'''
    p[0] = {
        'identifier': p[1],
        'type': 'NUMERIC',
        'precision': p[4],
        'scale': p[6]
    }

def p_column_def_create_date_default(p) -> None:
    '''column_def_create : IDENTIFIER DATE DEFAULT CURRENT_DATE'''
    p[0] = {
        'identifier': p[1],
        'type': 'DATE',
        'default': p[4]
    }

def p_column_def_create_date_simple(p) -> None:
    '''column_def_create : IDENTIFIER DATE'''
    p[0] = {
        'identifier': p[1],
        'type': 'DATE',
        'default': None
    }

# ======= LISTY KOLUMN ===========

def p_column_list_def_create_single(p) -> None:
    '''column_list_def_create : column_def_create'''
    p[0] = [p[1]]

def p_column_list_def_create_multiple(p) -> None:
    '''column_list_def_create : column_list_def_create COMMA column_def_create'''
    p[1].append(p[3])
    p[0] = p[1]


# =======================================
#           REGUŁY INSERT
# =======================================

def p_column_list_def_insert_single(p) -> None:
    '''column_list_def_insert : '''



parser = yacc.yacc()