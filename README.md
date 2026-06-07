# GitHub Actions - Zadanie 2

Workflow jest dostępny [tutaj](.github/workflows/docker-build.yml), repozytorium [tutaj](https://github.com/yel0h/ghactions-weather-app/pkgs/container/ghactions-weather-app).

Budowany obraz wspiera architektury linux/amd64 i linux/arm64. Repozytorium cache znajduje się [tutaj](https://hub.docker.com/r/yeloh/weather-app-cache). Skanowanie odbywa się przy pomocy Trivy z uwagi na prostszą
konfigurację i wydajność. Skan przeprowadzany jest na architekturze linux/amd64, aby zoptymalizować czas wykonania workflowa, ponieważ znaczna większość CVE jest niezależna od architektury, a dodatkowo Docker Buildx nie
pozwala eksportować wieloarchitekturowo do type=docker. Z tego względu przy budowie obrazu do przeskanowania cache jest tylko odczytywany, ale nie zapisywany.

W repozytorium zostały zdefiniowane sekrety `DOCKERHUB_USERNAME` i `DOCKERHUB_TOKEN`.

## Strategia tagowania obrazów

Zastosowano automatyczne tagowanie:
- latest, aby wskazać najnowszą wersję obrazu,
- \<nazwa_galezi\>, żeby móc zidentyfikować gałąź, do której push spowodował uruchomienie workflowa,
- sha-\<commit\>, co pozwala na pełną identyfikowalność wersji.

Dane cache są tagowane pojedynczym, stałym tagiem (cache), co upraszcza konfigurację pipeline'a i umożliwia ich współdzielenie między buildami.
