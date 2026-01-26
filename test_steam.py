import string
import pytest
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSteamStore:
    BASE_URL = "https://store.steampowered.com"

    def _generate_random_login_password(self):
        login_length = random.randint(8, 15)
        login = ''.join(random.choices(string.ascii_letters + string.digits, k=login_length))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=login_length))
        return login, password

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

        assert submit_btn.is_displayed(), "Кнопка авторизации неактивна"

        submit_btn.click()

        # Проверка что кнопка блокируется (появляется занчок загрузки)
        try:
            WebDriverWait(driver, 5).until_not(EC.element_to_be_clickable(submit_btn))
            wait.until(EC.element_to_be_clickable(submit_btn))
        except:
            try:
                WebDriverWait(driver, 5).until(
                    lambda d: submit_btn.get_attribute("disabled") is not None
                )

                wait.until(
                    lambda d: submit_btn.get_attribute('disabled') is None
                )
            except:
                print("Кнопка не блокируется")

        # Проверка ошибки через подсветку полей красной рамкой
        def has_error_style(element):
            try:
                border_color = element.value_of_css_property("border-color")
                print(f"проверка цвета рамки: {border_color}")
                if border_color:
                    if "193, 87, 85" in border_color:
                        return True
                    if "#c15755" in border_color.lower():
                        return True
                    if "255," in border_color or "#ff" in border_color.lower():
                        return True
                return False
            except Exception as e:
                print(f"Ошибка проверки рамки: {e}")
                return False

        if has_error_style(password_field):
            print("Поле пароля имеет красную рамку")
        else:
            wait.until(lambda d: has_error_style(password_field))
            print("Поле пароля получило красную рамку")

        # Проверка текста ошибки (только для русского, у этого элемента нет никаких тегов для поиска)
        error_element = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//div[ contains(text(), 'проверьте')]"
        )))
        error_text = error_element.text.strip()
        expected_phrases = ['проверьте', 'парол', 'аккаунт', 'попробуйте']
        for phrase in expected_phrases:
            assert phrase in error_text.lower(), f"Текст ошибки должен содержать '{phrase}'"

        assert wait.until(EC.element_to_be_clickable(submit_btn))
        print("Кнопка снова активна")
        assert "login" in driver.current_url.lower() or "signin" in driver.current_url.lower()
        print("Остались на странице авторизации")
