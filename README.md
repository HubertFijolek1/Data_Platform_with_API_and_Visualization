# Data Analysis Platform

## Opis
Platforma umożliwiająca przesyłanie danych, ich analizę oraz wizualizację wyników. Oferuje REST API do przesyłania danych oraz moduły AI do analizy danych (predykcja, klasyfikacja).

## Technologie
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Baza Danych:** PostgreSQL
- **Konteneryzacja:** Docker
- **CI/CD:** GitHub Actions

## Instalacja
1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/HubertFijolek1/Data_Analysis_Platform_with_API_and_Visualization.git
    cd Data_Analysis_Platform_with_API_and_Visualization
    ```

2. Uruchom Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Aplikacja będzie dostępna pod adresem `http://localhost:8000` dla backendu i `http://localhost:8501` dla frontend.

## Użycie
- Backend API jest dostępne pod `/docs` dla interaktywnej dokumentacji Swagger.
- Frontend umożliwia przesyłanie danych i wizualizację wyników analizy.

## Testy
Aby uruchomić testy backendu:
    ```bash
    cd backend
    pytest
    ```

## Generating Synthetic Data

To generate synthetic users and datasets, run the following script:

```bash
python scripts/generate_fake_data.py --users 200 --datasets 100
