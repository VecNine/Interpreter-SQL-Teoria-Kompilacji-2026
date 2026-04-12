import csv
import random

FILE_NAME = "pracownicy.csv"
ROW_COUNT = 100

IMIONA = ["Jan", "Anna", "Piotr", "Maria", "Krzysztof", "Katarzyna", "Marek", "Małgorzata", "Tomasz", "Agnieszka"]
NAZWISKA = ["Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński", "Lewandowski", "Zieliński",
            "Szymański", "Woźniak"]
STANOWISKA = ["Programista", "Tester", "Manager", "Analityk", "Designer", "HR", "Księgowy"]


def generate_csv():
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(["id", "imie", "nazwisko", "wiek", "stanowisko", "wyplata"])

        for i in range(1, ROW_COUNT + 1):
            id_pracownika = i
            imie = random.choice(IMIONA)
            nazwisko = random.choice(NAZWISKA)
            wiek = random.randint(18, 65)
            stanowisko = random.choice(STANOWISKA)
            wyplata = round(random.uniform(3500.0, 15000.0), 2)

            writer.writerow([id_pracownika, imie, nazwisko, wiek, stanowisko, wyplata])

    print(f"Plik '{FILE_NAME}' został pomyślnie wygenerowany ({ROW_COUNT} wierszy).")


if __name__ == "__main__":
    generate_csv()