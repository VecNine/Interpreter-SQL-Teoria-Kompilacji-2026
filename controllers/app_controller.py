from dataclasses import dataclass
from pyexpat.errors import messages
from typing import Any
import pandas as pd

from controllers.components.query_response import QueryResponse
from controllers.config.config import markdown_conf
from errors.errors import SqlSyntaxError
from executor.engine import CSVEngine

class AppController:

    # ==========================================
    # METODY DLA FRONTENDU (API Kontrolera)
    # ==========================================

    def __init__(self, st, height = 500):
        self.MAX_HEIGHT = height
        self.st = st

        self.st.markdown(markdown_conf, unsafe_allow_html=True)

        if 'last_dataframe' not in self.st.session_state:
            self.st.session_state.last_dataframe = None

    @property
    def last_dataframe(self):
        return self.st.session_state.last_dataframe

    @last_dataframe.setter
    def last_dataframe(self, value):
        self.st.session_state.last_dataframe = value

    def change_dir(self, new_path):
        self.st.session_state.current_path = new_path
        self.st.session_state.selected_full_path = ""

    @staticmethod
    def return_quoted_path(path):
        return f'"{path}"'

    def execute_sql_callback(self):
        """Funkcja wywoływana przez naciśnięcie Enter w polu tekstowym."""
        query = self.st.session_state.sql_editor

        if query:
            try:
                query_response = AppController.return_response(query)

                if query_response.status == "success":
                    self.last_dataframe = query_response.data
                if query_response.status == "error":
                    self.st.session_state.last_status = f"❌ Błąd: {query_response.message}"
                if query_response.status == "warning":
                    self.last_dataframe = query_response.data
                    self.st.session_state.last_status = f"⚠️ Ostrzeżenie: {query_response.message}"
                print(query)
            except Exception as e:
                self.st.session_state.last_status = f"❌ Błąd: {e}"




    # ==========================================
    # METODY DLA BACKENDU
    # ==========================================

    @staticmethod
    def return_response(sql_query: str) -> QueryResponse:
        """Przyjmuje SQL Query, zwraca QueryResponse"""

        # To jest taki tymczasowy, abym miał jak testowac
        df_mock = pd.DataFrame({
            "abc": [1, 2, 3],
            "bcd": [2, 3, 5],
            "efd": [2, 34, 4]
        })

        return QueryResponse(
            status="success",
            message="",
            ast=None,
            data=df_mock
        )