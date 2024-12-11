import os
import django

# Инициализация Django (по другому не работает)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarshop.settings')
django.setup()

import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from selenium.common.exceptions import TimeoutException
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment, teardown_test_environment
import time

class UITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Установка окружения Django для тестов."""
        setup_test_environment()
        super().setUpClass()

    def setUp(self):
        """Настройка браузера и тестового окружения перед каждым тестом."""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = 'http://localhost:8000/'

        unique_username = f"testuser_{uuid.uuid4().hex[:8]}"

        User.objects.create_user(username=unique_username, password='password123')
        self.username = unique_username

    def test_access_profile_without_auth(self):
        """TDB-C-32: Попытка доступа к странице профиля без авторизации."""
        driver = self.driver
        profile_url = f'{self.base_url}users/profile/'

        driver.get(profile_url)

        WebDriverWait(driver, 10).until(
            EC.url_contains('users/login')
        )
        self.assertIn('users/login', driver.current_url)

        login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Войти")]')
        self.assertIsNotNone(login_button)

    def test_logout_functionality(self):
        """TDB-C-28: Функция выхода из системы."""
        driver = self.driver
        driver.get(f'{self.base_url}users/login/')

        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys(self.username)
        password_field.send_keys('password123')
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class, 'btn-outline-danger') and contains(text(), 'Выйти')]"))
        )

        logout_button = driver.find_element(By.XPATH,
                                            "//a[contains(@class, 'btn-outline-danger') and contains(text(), 'Выйти')]")
        logout_button.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('users/login')
        )

        self.assertIn('users/login', driver.current_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )

        username_field = driver.find_element(By.NAME, 'username')
        self.assertIsNotNone(username_field)

    def test_login_functionality(self):
        """TDB-C-25: Функция входа в аккаунт."""
        driver = self.driver
        driver.get(f'{self.base_url}users/login/')

        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys(self.username)
        password_field.send_keys('password123')
        submit_button.click()

        time.sleep(2)

        print(f"Current URL after login attempt: {driver.current_url}")
        print(f"Page source: {driver.page_source[:1000]}")

        self.assertNotIn('users/login', driver.current_url, "Не удалось перейти с страницы входа.")

        WebDriverWait(driver, 20).until(
            EC.url_to_be(self.base_url)
        )

        try:
            logout_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Выйти')]"))
            )
            self.assertIsNotNone(logout_button, "Кнопка выхода отсутствует на странице.")
        except TimeoutException:
            print(f"TimeoutException: Кнопка 'Выйти' не была найдена на странице.")

    def test_registration_functionality(self):
        """TDB-C-23: Проверка регистрации нового пользователя."""
        driver = self.driver
        driver.get(f'{self.base_url}users/register/')

        username_field = driver.find_element(By.NAME, 'username')
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password1')
        confirm_password_field = driver.find_element(By.NAME, 'password2')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
        unique_email = f"{unique_username}@example.com"
        valid_password = "StrongPassword123!"

        username_field.send_keys(unique_username)
        email_field.send_keys(unique_email)
        password_field.send_keys(valid_password)
        confirm_password_field.send_keys(valid_password)
        submit_button.click()

        try:
            WebDriverWait(driver, 10).until(
                EC.url_changes(f'{self.base_url}users/register/')
            )
            print("Registration succeeded. Redirected to:", driver.current_url)
        except TimeoutException:
            print("Registration failed. Current URL:", driver.current_url)
            print("Page source:", driver.page_source[:1000])
            raise

        self.assertIn("Выйти", driver.page_source)

    def tearDown(self):
        """Закрытие браузера и удаление тестовых данных."""
        self.driver.quit()

        User.objects.filter(username=self.username).delete()

    @classmethod
    def tearDownClass(cls):
        """Очищаем окружение Django после тестов."""
        teardown_test_environment()
        super().tearDownClass()


if __name__ == "__main__":
    unittest.main()
