# ========================================
# Pytest fixture

# Fixture (alebo „testovacia pomôcka“) je špeciálna funkcia, ktorá sa používa na prípravu prostredia pred spustením testu.
# Môže vracať hodnoty (napr. ovládač prehliadača, databázové spojenie) a automaticky sa spustí pred každým testom, ktorý ju potrebuje.
# Pomáha znižovať duplicitu a udržiavať testy čisté a prehľadné.
# ========================================
import os
import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# Fixture `driver` – spúšťa Chrome WebDriver s požadovanými nastaveniami.
# V prípade, že je nastavená premená HEADLESS=1 alebo bežíme v CI prostredí, použije sa bezhlavý mód.
@pytest.fixture
def driver():
    """
    Fixture `driver` – spúšťa Chrome WebDriver s požadovanými nastaveniami.
    V prípade, že je nastavená premená HEADLESS=1 alebo bežíme v CI prostredí, použije sa bezhlavý mód.
    """
    options = Options()
    options.add_argument("--window-size=1920,1080") # Nastaví veľkosť okna prehliadača na 1920x1080 pixelov
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless") # pridáva možnosť spustiť prehliadač v bezhlavom režime, teda bez GUI
    if os.getenv("CI") == "true":
        options.add_argument("--headless=new") # pridáva možnosť spustiť prehliadač v bezhlavom režime pre CI
        options.add_argument("--disable-gpu") # vypína používanie GPU
        options.add_argument("--no-sandbox") # vypína Chrome sandbox. Sandbox môže prekážať spusteniu v CI.
        options.add_argument("--disable-dev-shm-usage") # núti Chrome používať bežný súborový systém namiesto /dev/shm
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
