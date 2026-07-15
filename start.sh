#!/bin/bash

# Sprawdzenie, czy środowisko wirtualne istnieje, jeśli nie, jego utworzenie
if [ ! -d "venv" ]; then
    echo "Tworzenie wirtualnego środowiska (venv)..."
    python3 -m venv venv
fi

# Aktywacja środowiska
echo "Aktywowanie wirtualnego środowiska..."
source venv/bin/activate

# Instalacja zależności
echo "Instalowanie zależności..."
pip install -r requirements.txt

# Uruchomienie opóźnionego otwierania przeglądarki w tle
(sleep 2 && xdg-open http://127.0.0.1:5000) &

# Uruchomienie aplikacji Flask
echo "Uruchamianie serwera na http://127.0.0.1:5000"
python app.py
