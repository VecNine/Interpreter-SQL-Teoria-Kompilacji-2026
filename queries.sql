SELECT imie, nazwisko, wyplata
        FROM "pracownicy.csv"
        WHERE wiek >= 18
        AND wyplata < 10000000.0
        ORDER BY nazwisko DESC LIMIT 10;



SELECT imie, nazwisko, wyplata
        FROM "pracownicy.csv"
        WHERE wiek >= 19
        AND wyplata < 5000
        ORDER BY nazwisko DESC LIMIT 10;