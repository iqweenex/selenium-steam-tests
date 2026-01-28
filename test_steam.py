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

    def test_page_open(self, driver, wait):
        driver.get(self.BASE_URL)
        wait.until(
            EC.url_contains("store.steampowered.com")
        )
        assert "Steam" in driver.title, f"Title: {driver.title}"
        print("Страница загружена")

    def test_search_field_exist(self, driver, wait):
        driver.get(self.BASE_URL)
        search_field = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "form[role='search']")
        ))
        print(f"Поле поиска отображается")

    def test_button_login(self, driver, wait):
        faker = Faker()

        driver.get(self.BASE_URL)

        # Находим кнопку страницы авторизации и жмем ее
        login_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".global_action_link[href*='login']")
        ))
        login_button.click()

        wait.until(
            lambda d: "login" in d.current_url or "signin" in d.current_url
        )
        print("Страница авторизации загружена")

        # Ищем поля для пароля и логина и вводим сгенерированные фейкером
        password_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@type, 'password')]"))
        )
        password_field.send_keys(faker.password())

        username_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".login_featuretarget_ctn input[type='text']")
            )
        )
        username_field.send_keys(faker.user_name())

        # Находим и жмем кнопку войти
        submit_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".login_featuretarget_ctn button[type='submit']")
            )
        )
        submit_btn.click()

        # Появление элемента загрузки
        loader_element = (By.CSS_SELECTOR, "._1VLukpV8qjL4BULw7Zob_l.WYrJyNEVnjgAnMVZgvPeg")
        wait.until(EC.presence_of_element_located(loader_element))
        print("Элемент загрузки появился")
        # Ждем исчезновения элемента загрузки
        wait.until_not(EC.presence_of_element_located(loader_element))
        print("Элемент загрузки исчез")

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
