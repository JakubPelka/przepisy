# Instrukcja Zarządzania Przepisami i Wdrażania (Deploy) na GitHub Pages

Ponieważ GitHub Pages obsługuje tylko i wyłącznie strony statyczne (bez bazy danych i kodu backendowego), proces dodawania przepisów i aktualizowania strony wygląda następująco:

## Krok 1: Uruchomienie lokalnego panelu (tylko na Twoim komputerze)

1. Otwórz terminal w folderze z projektem (tam gdzie znajduje się plik `app.py`).
2. Aktywuj środowisko wirtualne i uruchom aplikację (jeśli korzystasz z systemu Linux/Mac):
   ```bash
   source venv/bin/activate
   python app.py
   ```
   (Na systemie Windows użyj `venv\Scripts\activate`)
3. Otwórz przeglądarkę na stronie: `http://127.0.0.1:5000`
4. Powinieneś zobaczyć panel zarządzania z możliwością dodawania, edycji oraz usuwania przepisów.

## Krok 2: Eksport przepisów do statycznego HTML

1. Po dodaniu nowych lub zmodyfikowaniu obecnych przepisów kliknij zielony przycisk **"Eksportuj do HTML"** w panelu admina.
2. Aplikacja automatycznie wygeneruje nowy, zaktualizowany plik `index.html`, zawierający wszystkie Twoje najnowsze przepisy, wraz z indeksami składników, podziałem na kategorie oraz poprawnie działającą wyszukiwarką.

## Krok 3: Wdrażanie zmian na GitHub Pages (Deploy)

Plik `index.html` jest już zaktualizowany, podobnie jak baza danych `recipes.db`. Teraz musisz wysłać te zmiany na GitHub:

1. W terminalu (w folderze projektu) wpisz następujące komendy:
   ```bash
   git add .
   git commit -m "Aktualizacja przepisów"
   git push origin main
   ```
   *(Pamiętaj, by upewnić się, czy gałąź nazywa się `main` czy `master` i odpowiednio zmienić w razie potrzeby)*

2. Gdy kod zostanie wysłany, **GitHub Pages** po krótkiej chwili automatycznie odświeży Twoją stronę opartą o zaktualizowany plik `index.html`. 

## Dlaczego nie ignorujemy `recipes.db` w .gitignore?
Zgodnie z prośbą o optymalne zarządzanie prawami i brakiem wrażliwości danych, baza `recipes.db` jest wysyłana na GitHub. Dzięki temu:
- Nawet jeśli zmienisz komputer, zawsze masz najnowszą bazę danych.
- Masz pełną historię wersji swoich przepisów, więc jeśli coś usuniesz przez pomyłkę w panelu i wyeksportujesz stronę, zawsze możesz cofnąć się w git do poprzedniego stanu pliku `recipes.db`.

Powyższy proces w pełni zapewnia całkowitą autonomię zarządzania z jednoczesnym wsparciem dla darmowego hostingu na GitHub Pages.
