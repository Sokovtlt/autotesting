
# Automatizované testovanie aplikácie Biometric

Tento projekt obsahuje automatizované testy pre webovú aplikáciu [https://demo.biometric.sk](https://demo.biometric.sk) pomocou knižnice `selenium` a `pytest`.

---

## Možnosť 1: Testovanie prihlásenia do aplikácie

### Test Case 1A – Úspešné prihlásenie do systému

**Predpoklad:**  
Používateľ je na stránke: https://demo.biometric.sk/

**Kroky:**
1. Zadať prihlasovacie meno do poľa **Meno / ID**
2. Zadať heslo do poľa **Heslo**
3. Kliknúť na tlačidlo **Prihlásiť**

**Očakávaný výsledok:**  
Používateľ bude presmerovaný na Dashboard:  
https://demo.biometric.sk/Pages/Dashboard

**Prihlasovacie údaje:**  
- Meno: `65`  
- Heslo: `Test1234`

---

### Test Case 1B – Neúspešné prihlásenie

**Cieľ:**  
Overiť, že systém správne reaguje na neplatné prihlasovacie údaje.

**Kroky:**
1. Zadať neplatné používateľské meno alebo heslo
2. Kliknúť na tlačidlo **Prihlásiť**

**Očakávaný výsledok:**  
- Používateľ zostane na prihlasovacej stránke
- Zobrazí sa chybové hlásenie s informáciou o nesprávnych údajoch

---

### Test Case 1C – Extra test - Neúspešné prihlásenie niekoľko pokusov

**Cieľ:**  
Overiť, či sa zakaždým zníži počet pokusov.

**Kroky:**
1. Zadať neplatné heslo
2. Kliknúť na tlačidlo **Prihlásiť**
3. Opakovať so rovnakým používateľským menom

**Očakávaný výsledok:**
- Používateľ zostane na prihlasovacej stránke
- Zobrazí sa chybové hlásenie s informáciou o nesprávnych údajoch
- Počet zostávajúcich pokusov sa zníži

---

## Možnosť 2: Testovanie jazykových mutácií

**Cieľ:**  
Overiť, že prepínanie jazykových verzií (sk, en, cz) funguje správne.

**Kroky:**
1. Prepnúť jazyk kliknutím na príslušný jazykový odkaz
2. Overiť, že:
   - Placeholdery a texty na stránke sa zmenia podľa zvoleného jazyka
3. Obnoviť stránku
4. Overiť, že jazyková mutácia zostala zachovaná

---

## Spustenie testov

1. Aktivuj virtuálne prostredie:
```bash
source venv/bin/activate
```

2. Nainštaluj závislosti:
```bash
pip install -r requirements.txt
```

3. Spusť testy:

   Bez GUI
```bash
pytest tests/ --verbose -s
```

   Spusť testy s GUI:
```bash
HEADLESS=1 pytest tests/ --verbose -s
```

---

## 📁 Štruktúra priečinkov

```
autotesting/
│
├── tests/               # Obsahuje testovacie súbory
├── venv/                # Virtuálne prostredie
├── requirements.txt     # Zoznam závislostí
└── README.md            # Tento súbor
```

---

## 🔍 Prečo som si vybral Pytest a Selenium

### ✅ Selenium
Selenium je overený a široko používaný nástroj na testovanie webových aplikácií. Vybral som ho preto, že:

- Umožňuje **realistickú interakciu s webovou stránkou**, ako to robí skutočný používateľ (zadávanie údajov, klikanie, overovanie textu).
- Podporuje **všetky hlavné prehliadače** (Chrome, Firefox, Edge), čo je dôležité pre testovanie kompatibility.
- Má rozsiahlu dokumentáciu a komunitu.

### ✅ Pytest
Pytest som zvolil ako testovací rámec, pretože:

- Je **jednoduchý na použitie** – testy sú prehľadné, čitateľné a rýchlo sa píšu.
- Podporuje **fixtures**, ktoré zjednodušujú opakované nastavenia (napr. inicializácia prehliadača).
- Má silnú integráciu s CI/CD nástrojmi (GitHub Actions, GitLab CI atď.).
- Výsledky testov sú **prehľadné a dobre logované**.

---

## 🧑‍💻 Autor

Sergej Sokov – 2025