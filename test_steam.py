import string
import pytest
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker



class TestSteamStore:
    BASE_URL = "https://store.steampowered.com"

    def _generate_random_login_password(self):
        faker = Faker()
        return faker.user_name(), faker.password()

    def test_page_open(self, driver):
        driver.get(self.BASE_URL)

        assert "Steam" in driver.title

        assert "store.steampowered.com" in driver.current_url

        print("Страница загружена")

    def test_search_field_exist(self, driver):
        driver.get(self.BASE_URL)
        search_field = driver.find_element(By.CSS_SELECTOR, "form[role='search']")
        assert search_field.is_displayed()
        print(f"Поле поиска отображается")

    def test_button_login(self, driver, wait):
        driver.get(self.BASE_URL)
        login_button = driver.find_element(By.CSS_SELECTOR, ".global_action_link[href*='login']")
        assert login_button.is_displayed(), "Кнопки входа нет"

        login_button.click()
        current_url = driver.current_url
        assert "login" in current_url or "signin" in current_url, "Переход не произошел"

        password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@type, 'password')]"))
        )
        print("Страница авторизации загружена")

        username_field = driver.find_element(
            By.CSS_SELECTOR,
            ".login_featuretarget_ctn input[type='text']")
        assert username_field.is_displayed(), "Поле ввода логина не найдено"

        random_login, random_password = self._generate_random_login_password()
        username_field.send_keys(random_login)
        password_field.send_keys(random_password)

        submit_btn = driver.find_element(
            By.CSS_SELECTOR,
            ".login_featuretarget_ctn button[type='submit']")

        assert submit_btn.is_displayed(), "Кнопка авторизации невидна"

        submit_btn.click()

        # Проверка что кнопка блокируется (появляется элемент загрузки)
        try:
            WebDriverWait(driver,5).until_not(EC.element_to_be_clickable(submit_btn))
            wait.until(EC.element_to_be_clickable(submit_btn))
            print("Элемент загрузки появился и пропал, кнопка снова активна")
        except TimeoutException:
            print("Кнопка не заблокировалась или не разблокировалась после нажатия")

        # Проверка текста ошибки
        error_element = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class, '_1W_6HXiG4JJ0By1qN_0fGZ')]"
        )))
        error_text = error_element.text.strip()
        expected_error_text = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."
        assert error_text == expected_error_text, 'Текст ошибки не совпадает с ожидаемым'
        print("Текст появился")

        assert wait.until(EC.element_to_be_clickable(submit_btn))
        print("Кнопка снова активна")
        assert "login" in driver.current_url.lower() or "signin" in driver.current_url.lower()
        print("Остались на странице авторизации")
