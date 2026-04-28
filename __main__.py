from parser.parser import parser
from lexer.lexer import lexer
import pprint
import sys


def run_sql_file(file_path):
    try:

        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        print(f"--- Wczytano skrypt z pliku: {file_path} ---")

        ast = parser.parse(sql_script)

        if ast:
            print(f"Poprawnie sparsowano {len(ast)} zapytań.")
            for i, query in enumerate(ast, 1):
                print(f"\nZapytanie nr {i}:")
                print(query)

    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {file_path}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    run_sql_file("queries.sql")