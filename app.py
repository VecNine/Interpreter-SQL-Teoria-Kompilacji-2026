import streamlit as st
import pandas as pd
import os

from controllers.app_controller import AppController
from controllers.config.config import markdown_hide_button



app_controller = AppController(st)

if 'current_path' not in st.session_state:
    st.session_state.current_path = os.getcwd()
if 'selected_full_path' not in st.session_state:
    st.session_state.selected_full_path = ""
if 'sql_editor' not in st.session_state:
    st.session_state.sql_editor = "SELECT * FROM "


# Przyciski nawigacji
col1, col2 = st.columns([1, 5])
with col1:
    parent_dir = os.path.dirname(st.session_state.current_path)
    if st.button("⬅️ W górę"):
        app_controller.change_dir(parent_dir)

st.set_page_config(layout="wide")


col_left, col_right = st.columns([2, 8])

# ==========================================
#        GŁÓWNE OKNO Z DATAFRAME
# ==========================================

with col_right:
    with st.container(border=True, height=app_controller.MAX_HEIGHT):
        try:
            if app_controller.last_dataframe is not None:
                st.dataframe(app_controller.last_dataframe, height=app_controller.MAX_HEIGHT)
            else:
                st.dataframe(pd.DataFrame(), height=app_controller.MAX_HEIGHT)

        except Exception as e:
            st.error(f"Nieznany błąd w tworzeniu kontenera na SQL: {e}")


# ==========================================
#        GŁÓWNE OKNO Z PLIKAMI
# ==========================================


with col_left:
    with st.container(border=True, height=app_controller.MAX_HEIGHT):
        try:
            all_items = os.listdir(st.session_state.current_path)
            items = [
                item for item in all_items
                if os.path.isdir(os.path.join(st.session_state.current_path, item))
                   or item.lower().endswith('.csv')
            ]
            items.sort(key=lambda x: os.path.isdir(os.path.join(st.session_state.current_path, x)), reverse=True)

            for item in items:
                full_path = os.path.join(st.session_state.current_path, item)
                is_dir = os.path.isdir(full_path)
                icon = "📁" if is_dir else "📊"
                is_selected = (full_path == st.session_state.selected_full_path)

                button_type = "primary" if is_selected else "secondary"

                if st.button(f"{icon} {item}", key=full_path, use_container_width=True, type=button_type):
                    if is_dir:
                        app_controller.change_dir(full_path)
                        st.rerun()
                    else:
                        st.session_state.selected_full_path = full_path
                        quoted_path = app_controller.return_quoted_path(full_path)
                        st.session_state.sql_editor = f'SELECT * FROM {quoted_path};'
                        st.rerun()

        except PermissionError:
            st.error("Brak dostępu do tego folderu.")
        except Exception as e:
            st.error(f"Wystąpił błąd: {e}")


# ==========================================
#        GŁÓWNE OKNO Z SQL
# ==========================================


with st.container(border=True):
    st.markdown(markdown_hide_button, unsafe_allow_html=True)
    if 'last_status' in st.session_state:
        if "❌" in st.session_state.last_status:
            st.error(st.session_state.last_status)
        else:
            st.success(st.session_state.last_status)

    with st.form("sql_form", border=False):
        st.text_input(
            "Query:",
            key="sql_editor"
        )
        st.form_submit_button("Wykonaj", on_click=app_controller.execute_sql_callback)