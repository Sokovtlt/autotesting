import os

import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()