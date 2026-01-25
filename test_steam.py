from selenium.webdriver.common.by import By
import pytest

class TestSteamStore:

    BASE_URL = "https://store.steampowered.com"

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


    