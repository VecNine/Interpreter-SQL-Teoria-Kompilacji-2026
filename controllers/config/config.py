markdown_conf = """
    <style>
    /* Zmiana koloru przycisku 'primary' na zielony */
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white;
        border-color: #28a745;
    }
    /* Efekt po najechaniu myszką */
    div.stButton > button[kind="primary"]:hover {
        background-color: #218838;
        border-color: #1e7e34;
        color: white;
    }
    </style>
"""

markdown_hide_button = """
        <style>
        div[data-testid="stFormSubmitButton"] {
            display: none;
        }
        </style>
"""