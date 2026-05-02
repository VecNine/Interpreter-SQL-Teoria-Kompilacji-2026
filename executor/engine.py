import pandas as pd
from streamlit import status

from controllers.components.query_response import QueryResponse
from errors.errors import SqlSyntaxError
from parser.parser import parser
from lexer.lexer import lexer
import csv
import json
import os

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
                        response = self.create(query)
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

    
        cond_type = conditions[0]

        if cond_type == 'LOGIC':
            _, operator, left, right = conditions
            if operator == 'AND':
                return self.check_condition(row, left) and self.check_condition(row, right)
            else:
                return self.check_condition(row, left) or self.check_condition(row, right)

        elif cond_type == 'RELATION':
            _, operator, column, value = conditions
            cell_value = row.get(column)

            if cell_value is None or cell_value == "":
                return False

            try:
                if isinstance(value, (int, float)):
                    actual_cell_value = float(cell_value)
                    actual_query_value = float(value)
                else:
                    actual_cell_value = str(cell_value)
                    actual_query_value = str(value)


                match operator:
                    case '<':
                        return actual_cell_value < actual_query_value
                    case '<=':
                        return actual_cell_value <= actual_query_value
                    case '>':
                        return actual_cell_value > actual_query_value
                    case '>=':
                        return actual_cell_value >= actual_query_value
                    case '=':
                        return actual_cell_value == actual_query_value
                    case '!=':
                        return actual_cell_value != actual_query_value

            except (ValueError, TypeError):
                return False

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
        table_name = query['table_name']
        if not table_name.lower().endswith('.csv'):
            table_name += '.csv'

        columns = query['columns']
        values = query['values']
        meta_path = table_name + ".meta.json"

        try:
            with open(table_name, mode='r', encoding='utf8') as f:
                reader = csv.reader(f)
                file_headers = next(reader)

            metadata = None
            if os.path.exists(meta_path):
                with open(meta_path, 'r', encoding='utf8') as f:
                    metadata = json.load(f)

            rows_to_write = []
            for i, row in enumerate(values):
                if len(columns) != len(row):
                    return QueryResponse(status='error',
                                         message=f'Błąd w rekordzie {i + 1}: Liczba wartości się nie zgadza.',
                                         data=None)

                row_map = dict(zip(columns, row))
                if metadata:
                    for col_name, val in row_map.items():
                        col_def = metadata['columns'].get(col_name)
                        if not col_def:
                            continue

                        if col_def['type'] == 'VARCHAR' and col_def.get('length'):
                            if len(str(val)) > col_def['length']:
                                return QueryResponse(status='error',
                                                     message=f"Błąd: Wartość '{val}' przekracza długość {col_def['length']} dla kolumny {col_name}",
                                                     data=None)
                        if col_def['type'] == 'NUMERIC':
                            try:
                                float(val)
                            except ValueError:
                                return QueryResponse(status='error',
                                                     message=f"Błąd: Kolumna {col_name} wymaga liczby, otrzymano '{val}'",
                                                     data=None)

                mapped_values = []
                for header in file_headers:
                    if header in row_map:
                        mapped_values.append(row_map[header])
                    elif metadata and metadata['columns'].get(header) and metadata['columns'][header].get('default'):
                        mapped_values.append(metadata['columns'][header]['default'])
                    else:
                        mapped_values.append('')

                rows_to_write.append(mapped_values)

            with open(table_name, mode='a', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerows(rows_to_write)

            return QueryResponse(status='success', message=f'Pomyślnie dodano {len(rows_to_write)} wierszy.',
                                 data=None)

        except Exception as e:
            return QueryResponse(status='error', message=f"Błąd INSERT: {str(e)}", data=None)


    def create(self,query):
        table_name = query['table_name']
        if not table_name.lower().endswith('.csv'):
            table_name += '.csv'
        metadata = {
            "table_name": table_name,
            "columns": {col['identifier']: col for col in query['columns']}
        }

        try:
            headers = list(metadata["columns"].keys())
            with open(table_name, 'w', newline='', encoding='utf8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

            meta_file = table_name + ".meta.json"
            with open(meta_file, 'w', encoding='utf8') as f:
                json.dump(metadata, f, indent=4)

            return QueryResponse(
                status='success',
                message=f"Utworzono tabelę {table_name} oraz plik metadanych.",
                data=None
            )

        except Exception as e:
            return QueryResponse(status='error', message=f"Błąd CREATE: {str(e)}", data=None)

    def drop(self,query):
        print(query)

    def delete(self,query):
        print(query)