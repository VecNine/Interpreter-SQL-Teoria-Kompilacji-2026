from dataclasses import dataclass
from typing import Any
import pandas as pd

from controllers.components.query_response import QueryResponse
from errors.errors import SqlSyntaxError
from executor.engine import CSVEngine


class AppController:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.engine = CSVEngine(csv_path)

        self.current_data: pd.DataFrame = self._load_csv()
        self.query_history: list[str] = []

    def _load_csv(self) -> pd.DataFrame:
        """Prywatna metoda ładująca plik do pamięci."""
        try:
            return pd.read_csv(self.csv_path)
        except FileNotFoundError:
            return pd.DataFrame()

    # ==========================================
    # METODY DLA FRONTENDU (API Kontrolera)
    # ==========================================

    def get_current_data(self) -> pd.DataFrame:
        """Zwraca aktualny stan tabeli."""
        return self.current_data

    def get_schema_info(self) -> list[str]:
        """Zwraca listę kolumn jako ściągawkę dla użytkownika."""
        if self.current_data.empty:
            return []
        return [f"{col} ({dtype})" for col, dtype in self.current_data.dtypes.items()]

    def get_history(self) -> list[str]:
        """Zwraca historię zapytań."""
        return self.query_history

    def process_query(self, sql_input: str) -> QueryResponse:
        """Główny punkt wejścia. Parsuje, wykonuje i raportuje."""
        if not sql_input.strip():
            return QueryResponse(status="warning", message="Wpisz kod SQL.")

        try:
            self.query_history.append(sql_input)

            ast = self.engine.parse_text(sql_input)

            result_df = self.engine.execute_ast(ast)

            if ast['type'] == 'SELECT':
                msg = f"Pobrano {len(result_df)} wierszy."
                return QueryResponse(status="success", message=msg, ast=ast, data=result_df)

            else:
                self.current_data = self._load_csv()
                msg = f"Operacja {ast['type']} zakończona sukcesem."
                return QueryResponse(status="success", message=msg, ast=ast, data=self.current_data)

        except SqlSyntaxError as e:
            return QueryResponse(status="error", message=str(e), ast=None, data=None)
        except Exception as e:
            return QueryResponse(status="error", message=f"Błąd silnika: {e}", ast=None, data=None)