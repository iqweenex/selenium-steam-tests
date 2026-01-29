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
    HOME_MAINCAP_LOCATOR = (By.XPATH, "//*[@id='home_maincap_v7']")
    SEARCH_FIELD_LOCATOR = (By.XPATH, "//form[@role='search']")
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//*[contains(@class, 'global_action_link') and contains(@href, 'login')]")
    PASSWORD_FIELD_LOCATOR = (By.XPATH, "//*[contains(@type, 'password')]")
    USERNAME_FIELD_LOCATOR = (By.XPATH, "//*[contains(@class, 'login_featuretarget_ctn')]//input[@type='text']")
    SUBMIT_BUTTON_LOCATOR = (By.XPATH, "//*[contains(@class, 'login_featuretarget_ctn')]//button[@type='submit']")
    LOADER_ELEMENT_LOCATOR = (By.XPATH, "//button[@type='submit']/div")
    ERROR_ELEMENT_LOCATOR = (
        By.XPATH,
        "//*[@data-featuretarget='login']"
        "//*[contains(text(), 'проверьте свой пароль') and contains(text(), 'попробуйте снова')]"
    )

    def test_page_steam(self, driver, wait):
        faker = Faker()
        # Загружаем страницу
        driver.get(self.BASE_URL)
        # Выбрали карусель предложений в качестве уникального элемента,
        # который больше нигде не повторяется и имеет уникальный id
        wait.until(EC.visibility_of_element_located(self.HOME_MAINCAP_LOCATOR))
        print("Страница загружена")

        search_field = wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD_LOCATOR))
        print(f"Поле поиска отображается")

        # Находим кнопку страницы авторизации и жмем ее
        login_button = wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON_LOCATOR))
        login_button.click()
        print("Переходим на сраницу авторизации")

        # Ищем поля для пароля и логина и вводим сгенерированные фейкером
        password_field = wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD_LOCATOR))
        print("Страница авторизации загружена")
        password_field.send_keys(faker.password())
        username_field = wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD_LOCATOR))
        username_field.send_keys(faker.user_name())

        # Находим и жмем кнопку войти
        submit_btn = wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON_LOCATOR))
        submit_btn.click()

        # Появление элемента загрузки
        wait.until(EC.visibility_of_element_located(self.LOADER_ELEMENT_LOCATOR))
        print("Элемент загрузки появился")
        # Ждем исчезновения элемента загрузки
        wait.until_not(EC.presence_of_element_located(self.LOADER_ELEMENT_LOCATOR))
        print("Элемент загрузки исчез")

        # Проверка текста ошибки
        error_element = wait.until(EC.visibility_of_element_located(self.ERROR_ELEMENT_LOCATOR))
        error_text = error_element.text.strip()
        expected_error_text = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."
        assert error_text == expected_error_text, \
            'Текст ошибки не совпадает с ожидаемым:\n' \
            f'Ожидаемый текст: {expected_error_text}\n' \
            f'Фактический текст: {error_text}'
        print("Текст появился")
        print('-' * 50)
        print("Тест завершен")
