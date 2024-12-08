from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time  # Импортируем time для задержек


class BlogUITests(unittest.TestCase):

    def setUp(self):
        """Настройка браузера перед тестами."""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = 'http://localhost:8000/'

    def test_view_blog_page(self):
        """Проверка перехода на страницу блога с главной страницы магазина."""
        driver = self.driver
        driver.get(self.base_url)

        # Явное ожидание наличия заголовка на главной странице
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )

        # Задержка для просмотра загрузки главной страницы
        time.sleep(2)

        blog_link = driver.find_element(By.LINK_TEXT, 'Блог')
        blog_link.click()

        # Задержка перед проверкой страницы блога
        time.sleep(2)

        # Явное ожидание заголовка на странице блога
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )

        # Задержка для просмотра загрузки страницы блога
        time.sleep(2)

        blog_title = driver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(blog_title, 'БЛОГ')

    def test_view_post_with_invalid_custom_id(self):
        """Попытка открыть пост с некорректным custom_id через URL (проверка 404)."""
        driver = self.driver
        invalid_custom_id = 'invalid_custom_id'

        # Формируем URL для некорректного ID
        post_url = f'{self.base_url}blog/post/{invalid_custom_id}/'

        # Переход по URL с некорректным ID
        driver.get(post_url)

        # Явное ожидание загрузки страницы
        time.sleep(2)

        # Проверка, что на странице отображается ошибка 404
        error_message = driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Page not found', error_message)  # Изменено на текст "Page not found"

    def tearDown(self):
        """Закрытие браузера после тестов."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

