RESERVED: dict = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'order': 'ORDER',
    'by': 'BY',
    'asc': 'ASC',
    'desc': 'DESC',
    'limit': 'LIMIT',
    'and': 'AND',
    'or': 'OR',

    # Komendy edytowania i tworzenia CSV
    'create': 'CREATE',
    'table': 'TABLE',
    'insert': 'INSERT',
    'into': 'INTO',
    'values': 'VALUES',
    'delete': 'DELETE',
    'drop': 'DROP',

    # Typy i własności
    'varchar': 'VARCHAR',
    'numeric': 'NUMERIC',
    'date': 'DATE',
    'default': 'DEFAULT',
    'current_date': 'CURRENT_DATE',

    'primary': 'PRIMARY',
    'key': 'KEY',
    'not': 'NOT',
    'null': 'NULL',
    'serial': 'SERIAL'
}

TOKENS: list = [
    'IDENTIFIER',
    'STRING',
    'INTEGER',
    'FLOAT',

    'EQUALS',          # =
    'NOT_EQUALS',      # !=
    'GREATER',         # >
    'LESS',            # <
    'GREATER_EQUALS',  # >=
    'LESS_EQUALS',     # <=

    'ASTERISK',        # *
    'COMMA',           # ,
    'SEMICOLON',       # ;

    'LPAREN',          # (
    'RPAREN',          # )
] + list(RESERVED.values())