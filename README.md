# Interpreter-SQL---Teoria-Kompilacji-2026

# Założenia programu - CSV-SQL Transpiler  

* **Ogólne cele programu:** Stworzenie narzędzia do analizy i zarządzania danymi w plikach tekstowych. Program pozwala na wykonywanie operacji SQL (podzbiór obejmujący: `SELECT`, `INSERT`, `DELETE`, `CREATE`,`DROP` wraz z klauzulami `WHERE`, `ORDER BY` i `LIMIT`) bezpośrednio na plikach `.csv` bez użycia relacyjnych baz danych.
* **Rodzaj translatora:** Kompilator źródło-źródło (transpiler) pełniący w trybie runtime rolę interpretera.
* **Planowany wynik działania programu:** Transpiler języka SQL do zoptymalizowanego kodu w języku Python. Wynikiem jest automatyczne wykonanie wygenerowanego kodu, co skutkuje wyświetleniem danych w konsoli lub fizyczną modyfikacją struktury i zawartości plików CSV.
* **Planowany język implementacji:** Python 3.12+.
* **Sposób realizacji skanera/parsera:** Użycie generatora parserów **PLY (Python Lex-Yacc)**. Skaner realizowany za pomocą `ply.lex`, a parser w oparciu o algorytm LALR(1) przy użyciu `ply.yacc`.



**Autorzy:**
* Wiktor Bukowski – `wikbukowski@student.agh.edu.pl`
* Jakub Bafia – `jbafia@student.agh.edu.pl`

###  Specyfikacja Tokenów

W poniższej tabeli zestawiono wszystkie leksemy obsługiwane przez projektowany podzbiór języka SQL wraz z dopasowującymi je wyrażeniami regularnymi (RegEx).

| Kategoria | Nazwa Tokenu (ID) | Wyrażenie Regularne | Przykłady / Opis |
| :--- | :--- | :--- | :--- |
| **Słowa kluczowe (DQL/Logika)** | `SELECT`, `FROM`, `WHERE`, `ORDER`, `BY`, `ASC`, `DESC`, `LIMIT`, `AND`, `OR` | `(?i)^<slowo>$` | Zapytania i filtrowanie (case-insensitive). |
| **Słowa kluczowe (DDL/DML)** | `CREATE`, `DROP`, `INSERT`, `INTO`, `TABLE`, `VALUES` | `(?i)^<slowo>$` | Zarządzanie strukturą i danymi. |
| **Typy i Atrybuty danych** | `VARCHAR`, `NUMERIC`, `DATE`, `DEFAULT`, `CURRENT_DATE` | `(?i)^<slowo>$` | Definicje kolumn (np. `VARCHAR(255)`, `NUMERIC(10,2)`). |
| **Operatory** | `EQUALS`, `NOT_EQUALS`, `GREATER_EQUALS`, `LESS_EQUALS`, `GREATER`, `LESS` | `=`, `!=`, `>=`, `<=`, `>`, `<` | Operatory porównania i relacji. |
| **Symbole** | `ASTERISK` | `\*` | Wybór wszystkich kolumn. |
| | `COMMA` | `,` | Separator elementów na listach. |
| | `SEMICOLON` | `;` | Znak kończący zapytanie. |
| | `LPAREN`, `RPAREN` | `\(`, `\)` | Nawiasy (parametry typów, listy wartości). |
| **Literały i Typy** | `FLOAT` | `-?\d+\.\d+` | Liczby zmiennoprzecinkowe, np. `3.14`, `-0.5`. |
| | `INTEGER` | `-?\d+` | Liczby całkowite, np. `42`, `-7`. |
| | `STRING` | `"[^"]*"` \| `'[^']*'` | Tekst w cudzysłowach lub apostrofach. |
| **Identyfikatory** | `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy tabel i kolumn, np. `users`, `first_name`. |


### Notacja generatora PLY

Poniżej przedstawiono gramatykę zapisaną w notacji `YACC`:

```/* Deklaracja tokenów */
%token SELECT FROM WHERE ORDER BY ASC DESC LIMIT AND OR
%token INSERT INTO VALUES CREATE DROP TABLE DELETE
%token VARCHAR NUMERIC DATE DEFAULT CURRENT_DATE
%token IDENTIFIER STRING INTEGER FLOAT
%token EQUALS NOT_EQUALS GREATER LESS GREATER_EQUALS LESS_EQUALS
%token ASTERISK COMMA SEMICOLON LPAREN RPAREN

/* Priorytety */
%left OR
%left AND

%%

/* Korzeń gramatyki */
program
    : querylist
    | /* empty */
    ;

querylist
    : querylist query SEMICOLON
    | query SEMICOLON
    ;

/* Typy zapytań */
query
    : SELECT column_list FROM STRING where_clause order_clause limit_clause
    | DROP TABLE IDENTIFIER
    | CREATE TABLE IDENTIFIER LPAREN column_list_def_create RPAREN
    | INSERT INTO IDENTIFIER LPAREN column_list_args_insert RPAREN VALUES column_list_items_insert
    | DELETE FROM STRING where_clause /* <--- DODAJ TĘ LINIĘ */
    ;

/* --- Logika SELECT --- */
column_list
    : ASTERISK
    | IDENTIFIER
    | column_list COMMA IDENTIFIER
    ;

where_clause
    : WHERE condition
    | empty
    ;

condition
    : condition AND condition
    | condition OR condition
    | IDENTIFIER operator value
    ;

operator
    : EQUALS | NOT_EQUALS | GREATER | LESS | GREATER_EQUALS | LESS_EQUALS
    ;

value
    : INTEGER | FLOAT | STRING
    ;

order_clause
    : ORDER BY IDENTIFIER ASC
    | ORDER BY IDENTIFIER DESC
    | empty
    ;

limit_clause
    : LIMIT INTEGER
    | empty
    ;

/* --- Logika CREATE --- */
column_list_def_create
    : column_def_create
    | column_list_def_create COMMA column_def_create
    ;

column_def_create
    : IDENTIFIER VARCHAR LPAREN INTEGER RPAREN
    | IDENTIFIER NUMERIC LPAREN INTEGER COMMA INTEGER RPAREN
    | IDENTIFIER DATE DEFAULT CURRENT_DATE
    | IDENTIFIER DATE
    ;

/* --- Logika INSERT --- */
column_list_args_insert
    : IDENTIFIER
    | column_list_args_insert COMMA IDENTIFIER
    ;

column_list_items_insert
    : LPAREN value_list RPAREN
    | column_list_items_insert COMMA LPAREN value_list RPAREN
    ;

value_list
    : value
    | value_list COMMA value
    ;

/* Reguły pomocnicze */
empty : ;

%%
