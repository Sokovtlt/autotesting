import uuid
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Config
BASE_URL = "https://demo.biometric.sk/"
EXPECTED_URL = "https://demo.biometric.sk/Pages/Dashboard"
EXPECTED_URL_AFTER_WRONG_DATA = "https://demo.biometric.sk/Pages/Account/Login?ReturnUrl=%2fPages%2fDashboard"
EXPECTED_TITLE = "Dashboard | Demo"
LOGIN = "65"
PASSWORD = "Test1234"
INVALID_PASSWORD = "wrong_pass"

INVALID_LOGIN = f"wrong_user_{uuid.uuid4().hex[:6]}"
INVALID_LOGIN_1 = f"70"

# Locators
LOGIN_FIELD_LOCATOR = (By.ID, "TextBoxUsername")
PASSWORD_FIELD_LOCATOR = (By.ID, "TextBoxPassword")
SUBMIT_BUTTON_LOCATOR = (By.ID, "Button1")
ERROR_MESSAGE_LOCATOR = (By.ID, "swal2-content")
ERROR_BUTTON_LOCATOR = (By.CLASS_NAME, "swal2-confirm")
EXPECTED_ERROR_SNIPPET = "zadali ste nesprávne meno alebo heslo"



def test_login(driver):
    """
    Testovacia prípadová štúdia: Prihlásenie s platnými údajmi

    Cieľ:
        Overiť, že používateľ sa úspešne prihlási s platnými prihlasovacími údajmi.

    Kroky:
        1. Otvoriť prihlasovaciu stránku.
        2. Zadať používateľské meno a heslo.
        3. Kliknúť na tlačidlo „Prihlásiť“.

    Očakávaný výsledok:
        - Používateľ je presmerovaný na Dashboard.
        - Titulok stránky je „Dashboard | Demo“.
    """

    # Открытие страницы
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # Ожидание и ввод логина
    login_input = wait.until(EC.visibility_of_element_located(LOGIN_FIELD_LOCATOR))
    assert login_input.is_enabled(), "Login input is not enabled"
    login_input.send_keys(LOGIN)
    assert login_input.get_attribute("value") == LOGIN, "Login input value mismatch"

    # Ввод пароля
    password_input = wait.until(EC.visibility_of_element_located(PASSWORD_FIELD_LOCATOR))
    assert password_input.is_enabled(), "Password input is not enabled"
    password_input.send_keys(PASSWORD)
    assert password_input.get_attribute("value") == PASSWORD, "Password input value mismatch"

    # Клик по кнопке входа
    submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR))
    submit_button.click()

    # Проверка URL после входа
    WebDriverWait(driver, 10).until(
        EC.url_to_be(EXPECTED_URL)
    )
    current_url = driver.current_url
    assert current_url == EXPECTED_URL, f"Expected URL: {EXPECTED_URL}, Actual URL: {current_url}"

    # Проверка заголовка
    current_title = driver.title
    assert current_title == EXPECTED_TITLE, f"Expected title: {EXPECTED_TITLE}, Actual title: {current_title}"


def test_login_invalid_credentials(driver):
    """
    Testovacia prípadová štúdia: Neplatné prihlasovacie údaje

    Cieľ:
        Overiť, že pri zadaní nesprávnych údajov sa zobrazí chybové hlásenie a používateľ zostane na prihlasovacej stránke.

    Kroky:
        1. Otvoriť prihlasovaciu stránku.
        2. Zadať neplatné používateľské meno a heslo.
        3. Kliknúť na tlačidlo „Prihlásiť“.

    Očakávaný výsledok:
        - Používateľ zostane na prihlasovacej stránke.
        - Zobrazí sa hlásenie s textom „Zadali ste nesprávne meno alebo heslo“.
    """


    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    EXPECTED_URL_AFTER_WRONG_DATA = "https://demo.biometric.sk/Pages/Account/Login?ReturnUrl=%2fPages%2fDashboard"

    # Ввод некорректного логина
    login_input = wait.until(EC.visibility_of_element_located(LOGIN_FIELD_LOCATOR))
    assert login_input.is_enabled(), "Login input is not enabled"
    login_input.send_keys(INVALID_LOGIN)
    assert login_input.get_attribute("value") == INVALID_LOGIN, "Login input value mismatch"

    # Ввод некорректного пароля
    password_input = wait.until(EC.visibility_of_element_located(PASSWORD_FIELD_LOCATOR))
    assert password_input.is_enabled(), "Password input is not enabled"
    password_input.send_keys(INVALID_PASSWORD)
    assert password_input.get_attribute("value") == INVALID_PASSWORD, "Password input value mismatch"

    # Попытка входа
    submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR))
    submit_button.click()

    assert driver.current_url == EXPECTED_URL_AFTER_WRONG_DATA, \
        f"Expected to stay on login page. Initial: {EXPECTED_URL_AFTER_WRONG_DATA}, Final: {driver.current_url}"

    time.sleep(3)

    # Проверка наличия сообщения об ошибке
    error_message = wait.until(EC.visibility_of_element_located(ERROR_MESSAGE_LOCATOR))

    assert error_message.is_displayed(), "Error message not displayed"
    actual_text = error_message.text.strip().lower()
    assert EXPECTED_ERROR_SNIPPET in actual_text, f"Unexpected error message content:\n{actual_text}"

    # кнопка ok
    error_ok_button = wait.until(EC.element_to_be_clickable(ERROR_BUTTON_LOCATOR))
    error_ok_button.click()
    assert wait.until(EC.invisibility_of_element(error_message)), "The message is still displayed"
    time.sleep(3)


def test_trying_counter(driver):
    """
    Testovacia prípadová štúdia: Počet zostávajúcich pokusov

    Cieľ:
        Overiť, že pri každom neúspešnom prihlásení sa počet zostávajúcich pokusov znižuje.

    Kroky:
        1. Otvoriť prihlasovaciu stránku.
        2. Zadať platné meno a neplatné heslo.
        3. Opakovať prihlásenie viackrát.
        4. Čítať text z hlásenia a overiť znižovanie počtu pokusov.

    Očakávaný výsledok:
        - Text „Zostávajúci počet pokusov: N“ sa objaví a N sa znižuje o 1 pri každom pokuse.
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # Первый ввод — чтобы получить текущее значение попыток
    login_input = wait.until(EC.visibility_of_element_located(LOGIN_FIELD_LOCATOR))
    login_input.clear()
    login_input.send_keys(INVALID_LOGIN_1)

    password_input = wait.until(EC.visibility_of_element_located(PASSWORD_FIELD_LOCATOR))
    password_input.clear()
    password_input.send_keys(INVALID_PASSWORD)

    submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR))
    submit_button.click()

    error_message = wait.until(EC.visibility_of_element_located(ERROR_MESSAGE_LOCATOR))
    assert error_message.is_displayed(), "Error message not displayed"
    initial_text = error_message.text.strip().lower()

    import re
    match = re.search(r"zostávajúci počet pokusov: (\d+)", initial_text)
    assert match, f"Could not find remaining attempts in message:\n{initial_text}"
    initial_count = int(match.group(1))

    # Закрытие сообщения
    error_ok_button = wait.until(EC.element_to_be_clickable(ERROR_BUTTON_LOCATOR))
    error_ok_button.click()
    wait.until(EC.invisibility_of_element(error_message))

    # Проверка убывания количества попыток
    for expected_count in range(initial_count - 1, initial_count - 3, -1):
        login_input = wait.until(EC.visibility_of_element_located(LOGIN_FIELD_LOCATOR))
        login_input.clear()
        login_input.send_keys(INVALID_LOGIN_1)

        password_input = wait.until(EC.visibility_of_element_located(PASSWORD_FIELD_LOCATOR))
        password_input.clear()
        password_input.send_keys(INVALID_PASSWORD)

        submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR))
        submit_button.click()

        assert driver.current_url == EXPECTED_URL_AFTER_WRONG_DATA, \
            f"Expected to stay on login page. Final: {driver.current_url}"

        error_message = wait.until(EC.visibility_of_element_located(ERROR_MESSAGE_LOCATOR))
        assert error_message.is_displayed(), "Error message not displayed"
        actual_text = error_message.text.strip().lower()
        assert f"zostávajúci počet pokusov: {expected_count}" in actual_text, \
            f"Expected try count {expected_count} not found in message:\n{actual_text}"

        error_ok_button = wait.until(EC.element_to_be_clickable(ERROR_BUTTON_LOCATOR))
        error_ok_button.click()
        wait.until(EC.invisibility_of_element(error_message))
