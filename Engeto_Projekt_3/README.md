Automatizované testy – ENGETO

Tento projekt obsahuje automatizované end-to-end testy webu https://engeto.cz
.
Testy jsou napsané v Pythonu pomocí Playwright a pytest.

Cílem projektu je ověřit základní funkčnost webu z pohledu uživatele.

# Použité technologie

Python

Playwright (sync API)

Pytest

# Co projekt testuje
1) Otevření stránky Testing Akademie

Hover nad položku Kurzy

Kliknutí na Testing Akademie

Ověření správného nadpisu stránky

2) Odběr newsletteru

Vyplnění náhodně generovaného e-mailu

Odeslání formuláře

Ověření potvrzovací zprávy

3) Filtrování kurzů

Otevření stránky Zobrazit termíny kurzů

Výběr filtrů (Python, Testování softwaru)

Kliknutí na Zrušit filtry

Ověření, že filtry byly zrušeny

# Spuštění testů
pytest


Testy se spouští v ne-headless režimu pro lepší přehlednost.