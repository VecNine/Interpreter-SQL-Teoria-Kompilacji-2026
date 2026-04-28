from parser.parser import parser
from lexer.lexer import lexer
import pprint

if __name__ == '__main__':


    sql_query = '''
                SELECT imie, nazwisko, wyplata
                FROM "pracownicy.csv"
                WHERE wiek >= 18
                  AND wyplata < 5000.50
                ORDER BY nazwisko DESC LIMIT 10;
                '''

    wynik = parser.parse(sql_query, lexer=lexer)

    if wynik:
        print(wynik)