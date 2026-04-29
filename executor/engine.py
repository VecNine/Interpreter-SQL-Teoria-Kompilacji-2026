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

    def execute(self):
        print("execute")
        if self.parsed:
            for query in self.parsed:
                match query['type']:
                    case 'SELECT':
                        self.select(query)
                    case 'INSERT':
                        self.insert(query)

                    case 'CREATE':
                        self.create(query)

                    case 'DROP':
                        self.drop(query)

                    case 'DELETE':
                        self.delete(query)

        else:
            print("Brak zapytań do wyświetlenia.")

    def check_condtition(self, row, conditions) -> bool:
        if conditions is None:
            return True

        type = conditions[0]

    def select(self, query):
        file_name = query['from']
        columns_to_show = query['select']
        conditions = query['where']
        order_by = query['order']
        limit = query['limit']

        try:
            with open(file_name, 'r', encoding='utf8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
                print(data)

            filtered_data = [row for row in data if self.check_condition(row, conditions)]
        except FileNotFoundError:
            print("nima pliku")

    def insert(self, query):
        print(query)

    def create(self,query):
        print(query)

    def drop(self,query):
        print(query)

    def delete(self,query):
        print(query)