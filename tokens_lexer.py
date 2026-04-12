
reserved: dict = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'order': 'ORDER',
    'by': 'BY',
    'asc': 'ASC',
    'desc': 'DESC',
    'limit': 'LIMIT',
    'and': 'AND',
    'or': 'OR'
}

TOKENS: list = [
    'IDENTIFIER',
    'STRING',
    'INTEGER',
    'FLOAT',

    'EQUALS',           # =
    'NOT_EQUALS',       # !=
    'GREATER',          # >
    'LESS',             # <
    'GREATER_EQUALS',   # >=
    'LESS_EQUALS',      # <=

    'ASTERISK',         # *
    'COMMA'             # ,
] + list(reserved.values()) # Doklejenie wszystkich słów kluczowych do głównej listy