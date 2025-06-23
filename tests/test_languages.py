from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Конфигурация
BASE_URL = "https://demo.biometric.sk/"

CZ_LANGUAGE_LOCATOR = (By.XPATH, "//a[@href='?language=czech']")
EN_LANGUAGE_LOCATOR = (By.XPATH, "//a[@href='?language=english']")
SK_LANGUAGE_LOCATOR = (By.XPATH, "//a[@href='?language=slovak']")

LOGIN_FIELD_LOCATOR = (By.ID, "TextBoxUsername")
PASSWORD_FIELD_LOCATOR = (By.ID, "TextBoxPassword")
CHECKBOX_LOCATOR = (By.XPATH, "//label[@class='checkbox checkbox-outline checkbox-white text-white m-0']")
FORGET_PASS_LOCATOR = (By.ID, "LabelForgetPassword")
SUBMIT_BUTTON_LOCATOR = (By.ID, "Button1")
ERROR_MESSAGE_LOCATOR = (By.ID, "swal2-content")
ERROR_BUTTON_LOCATOR = (By.CLASS_NAME, "swal2-confirm")


def test_language_switch(driver):
    """
    Testovacia prípadová štúdia: Prepínanie jazykových mutácií

    Cieľ:
        Overiť, že používateľ môže prepínať medzi jazykovými mutáciami (slovenčina, angličtina, čeština) a že obsah sa zodpovedajúcim spôsobom aktualizuje.

    Kroky:
        1. Na prihlasovacej stránke kliknúť na odkaz pre každý jazyk.
        2. Overiť, že:
            - placeholder pre prihlasovacie meno a heslo je správny
            - text pri checkboxe je v danom jazyku
            - text odkazu "Zabudnuté heslo" zodpovedá jazyku
            - text na tlačidle "Prihlásiť" je správny
            - titulok stránky sa zmení podľa zvoleného jazyka
        3. Obnoviť stránku a znova overiť titulok.

    Očakávaný výsledok:
        - Všetky textové prvky a titulok sú zobrazené v zvolenom jazyku.
        - Po obnovení stránky zostane jazyková mutácia zachovaná.
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    language = {
        "czech": {
            "login_placeholder":  "Jméno / ID",
            "password_placeholder": "Heslo",
            "checkbox_label_text": "Neodhlašovat",
            "forget_pass_text": "Zapomenuté Heslo",
            "submit_button_value": "Přihlásit",
            "title": "Přihlášení do systému - Dochadzka.DEMO"
        },
        "english": {
            "login_placeholder":  "Name / ID",
            "password_placeholder": "Password",
            "checkbox_label_text": "Do not log out",
            "forget_pass_text": "Forget Password",
            "submit_button_value": "Login",
            "title": "Log on to the system - Dochadzka.DEMO"
        },
        "slovak": {
            "login_placeholder":  "Meno / ID",
            "password_placeholder": "Heslo",
            "checkbox_label_text": "Neodhlasovať",
            "forget_pass_text": "Zabudnuté Heslo",
            "submit_button_value": "Prihlásiť",
            "title": "Prihlásenie do systému - Dochadzka.DEMO"
        },
    }

    for lang_name, lang_config in language.items():

        # Переключаем язык
        if lang_name == "czech":
            driver.find_element(*CZ_LANGUAGE_LOCATOR).click()
        elif lang_name == "english":
            driver.find_element(*EN_LANGUAGE_LOCATOR).click()
        elif lang_name == "slovak":
            driver.find_element(*SK_LANGUAGE_LOCATOR).click()

        wait.until(EC.visibility_of_element_located(LOGIN_FIELD_LOCATOR))
        login_input = driver.find_element(*LOGIN_FIELD_LOCATOR)
        assert login_input.get_attribute("placeholder") == lang_config["login_placeholder"], \
            f"{lang_name}: Unexpected login placeholder"

        wait.until(EC.visibility_of_element_located(PASSWORD_FIELD_LOCATOR))
        password_input = driver.find_element(*PASSWORD_FIELD_LOCATOR)
        assert password_input.get_attribute("placeholder") == lang_config["password_placeholder"], \
            f"{lang_name}: Unexpected password placeholder"

        wait.until(EC.visibility_of_element_located(CHECKBOX_LOCATOR))
        checkbox_label = driver.find_element(*CHECKBOX_LOCATOR)
        assert checkbox_label.text == lang_config["checkbox_label_text"], \
            f"{lang_name}: Unexpected checkbox label"

        wait.until(EC.visibility_of_element_located(FORGET_PASS_LOCATOR))
        forget_pass = driver.find_element(*FORGET_PASS_LOCATOR)
        assert forget_pass.text == lang_config["forget_pass_text"], \
            f"{lang_name}: Unexpected forget password text"

        wait.until(EC.visibility_of_element_located(SUBMIT_BUTTON_LOCATOR))
        submit_button = driver.find_element(*SUBMIT_BUTTON_LOCATOR)
        assert submit_button.get_attribute("value") == lang_config["submit_button_value"], \
            f"{lang_name}: Unexpected submit button text"

        assert driver.title == lang_config["title"], f"{lang_name}: Unexpected page title"

        # Обновление страницы и повторная проверка title
        driver.refresh()
        wait.until(EC.visibility_of_element_located(LOGIN_FIELD_LOCATOR))
        assert driver.title == lang_config["title"], f"{lang_name}: Title mismatch after refresh"
