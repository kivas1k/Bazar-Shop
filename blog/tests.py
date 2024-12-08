import os
import django

# Инициализация Django (по другому не работает)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarshop.settings')
django.setup()

from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Post
from django.urls import reverse


class PostModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        if User.objects.filter(username='admin').exists():
            User.objects.filter(username='admin').delete()

    @patch('django.db.models.Model.save')
    def test_create_post_with_existing_custom_id(self, mock_save):
        """Тестирование попытки создать пост с уже существующим custom_id."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        post1 = Post.objects.create(
            custom_id='existing_id',
            title='Test Post 1',
            content='Test content 1',
            author=admin_user
        )
        post2 = Post(
            custom_id='existing_id',
            title='Test Post 2',
            content='Test content 2',
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post2.full_clean()

    @patch('django.db.models.Model.save')
    def test_create_post_with_empty_custom_id(self, mock_save):
        """Тестирование создания поста с пустым полем custom_id."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        post = Post(
            custom_id='',
            title='Test Post',
            content='Test content',
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_create_post_with_valid_data(self):
        """Тестирование успешного создания поста с валидными данными."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        post = Post(
            custom_id='unique_id',
            title='Test Post',
            content='Test content',
            author=admin_user
        )
        post.save()

        saved_post = Post.objects.filter(custom_id='unique_id', title='Test Post').first()
        self.assertIsNotNone(saved_post)
        self.assertEqual(saved_post.author, admin_user)

    @patch('django.db.models.Model.save')  # Мокирование метода save
    def test_title_field_length(self, mock_save):
        """Тестирование длины поля title."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        long_title = 'a' * 256  # Длина больше чем максимальная (255 символов)
        post = Post(
            custom_id='unique_id',
            title=long_title,
            content='Test content',
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    @patch('django.db.models.Model.save')
    def test_custom_id_field_length(self, mock_save):
        """Тестирование длины поля custom_id."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        long_custom_id = 'a' * 256
        post = Post(
            custom_id=long_custom_id,
            title='Test Post',
            content='Test content',
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_successful_edit_post(self):
        """Тестирование успешного редактирования поста."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        post = Post.objects.create(
            custom_id='unique_id',
            title='Old Title',
            content='Test content',
            author=admin_user
        )
        post.title = 'New Title'
        post.save()
        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.title, 'New Title')

    @patch('django.db.models.Model.save')
    def test_create_post_without_required_fields(self, mock_save):
        """Тестирование создания поста без обязательных полей."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')

        post_missing_custom_id = Post(
            custom_id=None,
            title='Test Title',
            content='Test Content',
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post_missing_custom_id.full_clean()

        post_missing_title = Post(
            custom_id='unique_id',
            title=None,
            content='Test Content',
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post_missing_title.full_clean()

        post_missing_content = Post(
            custom_id='unique_id',
            title='Test Title',
            content=None,
            author=admin_user
        )
        with self.assertRaises(ValidationError):
            post_missing_content.full_clean()

        # Проверка отсутствия author
        post_missing_author = Post(
            custom_id='unique_id',
            title='Test Title',
            content='Test Content',
            author=None
        )
        with self.assertRaises(ValidationError):
            post_missing_author.full_clean()

    @patch('django.db.models.Model.save')
    @patch('django.db.models.Model.delete')
    def test_successful_delete_post(self, mock_delete, mock_save):
        """Тестирование успешного удаления поста."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        post = Post.objects.create(
            custom_id='unique_id',
            title='Test Post',
            content='Test content',
            author=admin_user
        )
        post_id = post.id
        post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post_id)

    @patch('django.db.models.Model.save')
    @patch('django.db.models.Model.delete')
    def test_post_after_delete(self, mock_delete, mock_save):
        """Тестирование получения поста после его удаления."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        post = Post.objects.create(
            custom_id='unique_id',
            title='Test Post',
            content='Test content',
            author=admin_user
        )
        post.delete()
        post = Post.objects.filter(id=post.id).first()
        self.assertIsNone(post)

    def test_create_post_as_regular_user(self):
        """Тестирование создания поста обычным пользователем (перенаправление на страницу входа)."""
        regular_user = User.objects.create_user(username='regularuser', password='password')
        self.client.login(username='regularuser', password='password')
        response = self.client.post(reverse('blog_create'))  # URL для создания поста
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление на страницу входа

    def test_edit_post_as_regular_user(self):
        """Тестирование редактирования поста обычным пользователем (перенаправление на страницу входа)."""
        regular_user = User.objects.create_user(username='regularuser', password='password')
        post = Post.objects.create(
            custom_id='unique_id',
            title='Test Post',
            content='Test content',
            author=regular_user
        )
        self.client.login(username='regularuser', password='password')
        response = self.client.post(reverse('blog_edit', args=[post.custom_id]))  # URL для редактирования поста
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление на страницу входа

    def test_delete_post_as_regular_user(self):
        """Тестирование удаления поста обычным пользователем (перенаправление на страницу входа)."""
        regular_user = User.objects.create_user(username='regularuser', password='password')
        post = Post.objects.create(
            custom_id='unique_id',
            title='Test Post',
            content='Test content',
            author=regular_user
        )
        self.client.login(username='regularuser', password='password')
        response = self.client.post(reverse('blog_delete', args=[post.custom_id]))  # URL для удаления поста
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление на страницу входа

    def test_post_update_after_edit(self):
        """Тестирование обновления поста после редактирования."""
        admin_user = User.objects.create_superuser(username='admin', password='admin123')

        # Создание поста
        post = Post.objects.create(
            custom_id='unique_id',
            title='Old Title',
            content='Test content',
            author=admin_user
        )

        post.title = 'Updated Title'
        post.content = 'Updated content'
        post.save()

        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.content, 'Updated content')

        self.assertNotEqual(updated_post.title, 'Old Title')
        self.assertNotEqual(updated_post.content, 'Test content')

