from executor.engine import CSVEngine
from parser.parser import parser
from lexer.lexer import lexer
import pprint

if __name__ == '__main__':

    engine = CSVEngine("""SELECT imie, nazwisko, wyplata
        FROM "pracownicy.csv"
        WHERE wiek >= 18
        AND wyplata < 10000000.0
        ORDER BY nazwisko DESC LIMIT 10;



SELECT imie, nazwisko, wyplata
        FROM "pracownicy.csv"
        WHERE wiek >= 19
        AND wyplata < 5000
        ORDER BY nazwisko DESC LIMIT 10;""")
    engine.parse()
    engine.execute()
