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
| **Słowa kluczowe** | `SELECT`, `FROM`, `WHERE`, `ORDER`, `BY`, `ASC`, `DESC`, `LIMIT`, `AND`, `OR` | `(?i)^<slowo>$` | Ignorują wielkość liter (np. `SELECT`, `select`, `SeLeCt`). |
| **Operatory** | `EQUALS` | `=` | Równość |
| | `NOT_EQUALS` | `!=` | Nierówność |
| | `GREATER_EQUALS` | `>=` | Większe lub równe |
| | `LESS_EQUALS` | `<=` | Mniejsze lub równe |
| | `GREATER` | `>` | Ostro większe |
| | `LESS` | `<` | Ostro mniejsze |
| **Symbole** | `ASTERISK` | `\*` | Wybór wszystkich kolumn |
| | `COMMA` | `,` | Separator na liście kolumn |
| | `SEMICOLON` | `;` | Separator między podzapytaniami |
| **Literały i Typy** | `FLOAT` | `-?\d+\.\d+` | Np. `3.14`, `-0.5` |
| | `INTEGER` | `-?\d+` | Np. `42`, `-7` |
| | `STRING` | `"[^"]*"` \| `'[^']*'` | Np. `"dane.csv"`, `'Kowalski'` |
| **Identyfikatory** | `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy kolumn, np. `imie`, `wiek` |


### Notacja generatora PLY

Poniżej przedstawiono gramatykę zapisaną w notacji `YACC`:

```/* Deklaracja tokenów (terminali) */
%token SELECT FROM WHERE ORDER BY ASC DESC LIMIT AND OR
%token IDENTIFIER STRING INTEGER FLOAT
%token EQUALS NOT_EQUALS GREATER LESS GREATER_EQUALS LESS_EQUALS
%token ASTERISK COMMA SEMICOLON

/* Definicja priorytetów operatorów logicznych */
%left OR
%left AND

%%

/* Reguły produkcji (gramatyka) */

program
    : querylist
    | /* empty */
    ;

querylist
    :querylist query SEMICOLON
    | query SEMICOLON
    ;

query
    : SELECT column_list FROM STRING where_clause order_clause limit_clause
    ;

column_list
    : ASTERISK
    | IDENTIFIER
    | column_list COMMA IDENTIFIER
    ;

where_clause
    : WHERE condition
    | /* empty */
    ;

condition
    : condition AND condition
    | condition OR condition
    | IDENTIFIER operator value
    ;

operator
    : EQUALS
    | NOT_EQUALS
    | GREATER
    | LESS
    | GREATER_EQUALS
    | LESS_EQUALS
    ;

value
    : INTEGER
    | FLOAT
    | STRING
    ;

order_clause
    : ORDER BY IDENTIFIER ASC
    | ORDER BY IDENTIFIER DESC
    | /* empty */
    ;

limit_clause
    : LIMIT INTEGER
    | /* empty */
    ;

%%```
