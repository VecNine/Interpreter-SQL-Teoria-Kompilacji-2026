import pandas as pd
from streamlit import status

from controllers.components.query_response import QueryResponse
from errors.errors import SqlSyntaxError
from parser.parser import parser
from lexer.lexer import lexer
import csv

class CSVEngine:
    query : str
    parsed : list[dict]

    def __init__(self, query):
        self.parsed = []
        self.query = query

    def parse(self):
        print(f"--- Wczytano skrypt ---")
        self.parsed = parser.parse(self.query, lexer=lexer)


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
                        response =  self.select(query)
                    case 'INSERT':
                        response = self.insert(query)
                    case 'CREATE':
                        print("do implementacji")
                        # response = self.create(query)
                    case 'DROP':
                        print("do implementacji")
                        # response = self.drop(query)
                    case 'DELETE':
                        print("do implementacji")
                        # response = self.drop(query)
                    case _:
                        response = QueryResponse(status='error', message='idk', data = None)


        else:
            response = QueryResponse(status='error', message='cos poszło nie tak', data=None)
            print("Brak zapytań do wyświetlenia.")
        return response

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

                def safe_sort_key(x):
                    val = x.get(col, "")
                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        return str(val)

                filtered_data.sort(
                    key=safe_sort_key,
                    reverse=(direction == "DESC")
                )

            if limit is not None:
                filtered_data = filtered_data[:limit]

            if filtered_data:
                df = pd.DataFrame(filtered_data)

                if columns_to_show != '*':
                    missing_cols = [c for c in columns_to_show if c not in df.columns]

                    if missing_cols:
                        return QueryResponse(
                            status='error',
                            message=f"Błąd: Nie znaleziono kolumn: {', '.join(missing_cols)}",
                            data=None
                        )
                    df = df[columns_to_show]

                return QueryResponse(status='success', message='Pobrano dane pomyślnie', data=df)
            else:
                return QueryResponse(status='success', message='Brak wyników spełniających kryteria',
                                     data=pd.DataFrame())

            # self._display_results(filtered_data, columns_to_show)

        except FileNotFoundError:
            return QueryResponse(status='error', message=str(SqlSyntaxError), data = None)

    # def _display_results(self, data, columns):
    #     if not data:
    #         print("brak wynikow")
    #         return
    #     header = data[0].keys() if columns == '*' else columns
    #     print(" | ".join(header))
    #     print("-" * (len(header) * 15))
    #
    #     for row in data:
    #         print(" | ".join(str(row.get(col, "")) for col in header))

    def insert(self, query):
        table_name : str
        table_name = query['table_name']
        columns = query['columns']
        values = query['values']

        if not table_name.lower().endswith('.csv'):
            table_name += '.csv'

        try:
            with open(table_name, mode='r', encoding='utf8') as f:
                reader = csv.reader(f)
                file_headers = next(reader)

            for col in columns:
                if col not in file_headers:
                    return QueryResponse(status='error', message=f"Kolumna '{col}' nie istnieje w {table_name}",
                                         data=None)
            rows_to_write = []
            for i, row in enumerate(values):
                if len(columns) != len(row):
                    return QueryResponse(
                        status = 'error',
                        message = f'Błąd w rekordzie nr {i+1}. Niepoprawna ilość argumentów. Podano {len(row)} a oczekiwano {len(columns)}',
                        data = None
                    )
                row_map = dict(zip(columns,row))
                mapped_values = [row_map.get(header,'') for header in file_headers]
                rows_to_write.append(mapped_values)

            with open(table_name, mode = 'a', newline='', encoding = 'utf8' ) as file:
                writer = csv.writer(file)
                writer.writerows(rows_to_write)
            return QueryResponse(
                status = 'success',
                message = 'Pomyślnie dodano podane wartości',
                data = None
            )


        except FileNotFoundError:

            return QueryResponse(status='error', message=f"Nie znaleziono pliku: {table_name}", data=None)

        except Exception as e:

            return QueryResponse(status='error', message=f"Błąd krytyczny zapisu: {str(e)}", data=None)



    def create(self,query):
        print(query)

    def drop(self,query):
        print(query)

    def delete(self,query):
        print(query)