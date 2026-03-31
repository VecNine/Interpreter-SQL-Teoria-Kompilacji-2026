# Interpreter-SQL---Teoria-Kompilacji-2026

# CSV-SQL Transpiler

## 1. Informacje ogólne

**Temat projektu:** Kompilator źródło-źródło (transpiler) podzbioru języka SQL do języka Python z bezpośrednią obsługą plików CSV.

**Autorzy:**
* Wiktor Bukowski – `wikbukowski@student.agh.edu.pl`
* Jakub Bafia – `jbafia@student.agh.edu.pl`

**Ogólne cele programu:**
Celem projektu jest stworzenie interpretera/transpilera, który pozwala na wykonywanie zapytań w języku SQL bezpośrednio na plikach tekstowych o rozszerzeniu `.csv`. Program przetłumaczy wejściowe zapytanie SQL na zoptymalizowany, natywny kod w języku Python, a następnie automatycznie go wykona, zwracając przefiltrowane i posortowane dane. Narzędzie ma ułatwić szybką analizę plików CSV bez konieczności importowania ich do klasycznych silników relacyjnych baz danych.

---

## 2. Wymagania funkcjonalne 

1. **Analiza leksykalna i składniowa:** Program musi poprawnie rozpoznawać tokeny i weryfikować składnię dla obsługiwanego podzbioru języka SQL.
2. **Obsługa klauzuli SELECT:** Możliwość wyboru konkretnych kolumn (np. `SELECT imie, nazwisko`) lub wszystkich dostępnych kolumn (`SELECT *`).
3. **Obsługa klauzuli FROM:** Wskazanie ścieżki do pliku CSV jako źródła danych (np. `FROM "dane.csv"`).
4. **Obsługa klauzuli WHERE:** Filtrowanie wierszy z wykorzystaniem:
   * Operatorów relacyjnych: `=`, `!=`, `>`, `<`, `>=`, `<=`
   * Operatorów logicznych: `AND`, `OR`
   * Rozpoznawania typów prostych (liczby całkowite, liczby zmiennoprzecinkowe, ciągi znaków).
5. **Obsługa klauzuli ORDER BY:** Sortowanie wyników rosnąco (`ASC`) lub malejąco (`DESC`) po wskazanej kolumnie.
6. **Obsługa klauzuli LIMIT:** Ograniczenie liczby zwracanych rekordów do podanej wartości całkowitej.
7. **Generacja kodu:** Generowanie poprawnego syntaktycznie kodu w języku Python realizującego logikę zapytania przy użyciu standardowej biblioteki `csv`.
8. **Wykonanie kodu (Runtime):** Automatyczne uruchomienie wygenerowanego skryptu i wypisanie wyników na standardowe wyjście (konsola) w czytelnej formie.

---

## 3. Wymagania niefunkcjonalne

1. **Język implementacji:** Python 3.12+ (ze względu na bogaty ekosystem narzędzi do parsowania i łatwość dynamicznego wykonywania wygenerowanego kodu).
2. **Zależności zewnętrzne:** Ograniczenie do minimum. Do przetwarzania danych wynikowych używana będzie wyłącznie standardowa biblioteka Pythona.
3. **Interfejs użytkownika:** Interfejs wiersza poleceń (CLI). Program powinien przyjmować zapytanie SQL jako argument wywołania lub czytać je z podanego pliku `.sql`.
4. **Obsługa błędów:** * Zrozumiałe komunikaty o błędach składniowych (wskazanie linii i znaku w zapytaniu SQL).
   * Komunikaty o błędach semantycznych (np. próba odwołania się do nieistniejącego pliku CSV lub nieistniejącej kolumny).

---

## 4. Wybór generatora parserów

Zgodnie z wymogami projektu oraz bazując na zestawieniu z artykułu *Comparison of parser generators* (Wikipedia), dokonano analizy dostępnych narzędzi potrafiących wygenerować kod parsera w języku **Python** (język docelowy implementacji naszego kompilatora).

Biorąc pod uwagę specyfikę języka Python oraz algorytmy parsowania, rozważano narzędzia wspierające generację kodu dla tego języka, takie jak ANTLR (LL(*)) oraz PLY (LALR(1)). 

**Decyzja:** Wybrano narzędzie **PLY (Python Lex-Yacc)**.

**Uzasadnienie:**
* **Zgodność języka:** PLY jest napisany w całości w Pythonie i generuje kod w Pythonie, co idealnie wpisuje się w nasze wymagania niefunkcjonalne.
* **Brak zewnętrznych zależności kompilacji:** W przeciwieństwie do np. ANTLR4, który do wygenerowania parsera wymaga środowiska Java (JRE), PLY korzysta z mechanizmów refleksji w Pythonie i buduje tabele parsowania "w locie" (lub cachuje je do plików), co znacznie ułatwia budowanie i uruchamianie projektu.
* **Algorytm:** PLY wykorzystuje klasyczny algorytm LALR(1) (podobnie jak Yacc/Bison), co jest w pełni wystarczające do zbudowania gramatyki bezkontekstowej dla wybranego podzbioru języka SQL i dobrze realizuje edukacyjne założenia przedmiotu Teoria Kompilacji.
