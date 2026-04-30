from parser.parser import parser
from lexer.lexer import lexer
import csv

class CSVEngine:
    query_path : str
    parsed : list[dict]

    def __init__(self, path):
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

    def check_condition(self, row, conditions) -> bool:
        if conditions is None:
            return True

        type = conditions[0]
        if type == 'LOGIC':
            _, operator, left, right = conditions
            if operator == 'AND':
                return self.check_condition(row,left) and self.check_condition(row,right)
            else:
                return self.check_condition(row,left) or self.check_condition(row,right)
        elif type == 'RELATION':
            _, operator,column , value = conditions

            cell_value = row.get(column)

            try:
                if isinstance(value, (int, float)):
                    cell_value = float(cell_value)
            except (ValueError, TypeError):
                pass

            match operator:
                case '<': return cell_value < value
                case '<=': return cell_value <= value
                case '>': return cell_value > value
                case '>=': return cell_value >= value
                case '=' : return cell_value == value
                case '!=' : return cell_value != value

        return False


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

            if order_by:
                col, direction = order_by
                filtered_data.sort(
                    key = lambda x: x.get(col, ""),
                    reverse=(direction == "desc")
                )

            if limit is not None:
                filtered_data = filtered_data[:limit]

            self._display_results(filtered_data, columns_to_show)

        except FileNotFoundError:
            print("nima pliku")

    def _display_results(self, data, columns):
        if not data:
            print("brak wynikow")
            return
        header = data[0].keys() if columns == '*' else columns
        print(" | ".join(header))
        print("-" * (len(header) * 15))

        for row in data:
            print(" | ".join(str(row.get(col, "")) for col in header))

    def insert(self, query):
        print(query)

    def create(self,query):
        print(query)

    def drop(self,query):
        print(query)

    def delete(self,query):
        print(query)