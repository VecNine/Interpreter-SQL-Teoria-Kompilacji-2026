from parser.parser import parser
from lexer.lexer import lexer

class CSVEngine:
    query_path : str
    parsed : list[dict]

    def __init__(self,path):
        self.parsed = []
        self.query_path = path

    def parse(self):
        try:
            with open(self.query_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            print(f"--- Wczytano skrypt z pliku: {self.query_path} ---")
            self.parsed = parser.parse(sql_script, lexer=lexer)


        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {self.query_path}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def print_queries(self):
        if self.parsed:
            for query in self.parsed:
                print(query)
        else:
            print("Brak zapytań do wyświetlenia.")
