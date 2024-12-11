import os
import django
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarshop.settings')
django.setup()

from unittest.mock import patch
from .models import UserProfile
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserRegistrationForm, UserProfileForm


def generate_random_username():
    """Генерация случайного имени пользователя для каждого теста."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


class UserRegistrationFormTestCase(TestCase):
    @patch('django.contrib.auth.models.User.objects.filter')
    def setUp(self, mock_filter):
        self.username = generate_random_username()
        mock_filter.return_value.exists.return_value = True
        User.objects.create_user(username=self.username, email='test@example.com', password='Password123!')

    def test_registration_with_invalid_email(self):
        """Тест регистрации пользователя с некорректным email."""
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'Password123!',
            'password2': 'Password123!',
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_with_missing_required_fields(self):
        """Тест регистрации пользователя с отсутствующими обязательными полями."""
        data = {}
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)

    @patch('django.contrib.auth.models.User.objects.filter')
    def test_registration_with_existing_email(self, mock_filter):
        """Тест регистрации с уже существующим email."""
        mock_filter.return_value.exists.return_value = True

        data = {
            'username': 'new_user',
            'email': 'test@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)  # Ошибка на email


class UserProfileFormTestCase(TestCase):
    @patch('django.db.models.Model.save')
    def setUp(self, mock_save):
        # Создание пользователя с уникальным именем
        self.username = generate_random_username()
        self.user = User.objects.create_user(username=self.username, password='Password123!')
        self.profile = UserProfile.objects.create(user=self.user)

    @patch('django.db.models.Model.save')
    def test_edit_profile_with_valid_data(self, mock_save):
        """Тест успешного редактирования профиля с валидными данными."""
        profile = self.user.profile
        form = UserProfileForm(instance=profile, data={'bio': 'New Bio', 'avatar': None})
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.bio, 'New Bio')
        mock_save.assert_called_once()

    @patch('django.db.models.Model.save')
    def test_edit_profile_with_empty_fields(self, mock_save):
        """Тест редактирования профиля с пустыми полями."""
        profile = self.user.profile
        form = UserProfileForm(instance=profile, data={'bio': '', 'avatar': None})
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.bio, '')
        mock_save.assert_called_once()


class LoginFormTestCase(TestCase):

    def setUp(self):
        self.username = generate_random_username()
        self.user = User.objects.create_user(username=self.username, password='Password123!')
        self.user.backend = 'django.contrib.auth.backends.ModelBackend'

    def test_login_with_invalid_credentials(self):
        """Тест входа с некорректными данными."""
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpassword'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')

    def test_login_with_valid_credentials(self):
        """Тест входа с корректными данными."""
        response = self.client.post(reverse('login'), {'username': self.username, 'password': 'Password123!'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        user = self.client.get(reverse('profile'))
        self.assertContains(user, 'Профиль пользователя')


class UnauthorizedProfileEditTestCase(TestCase):
    def test_edit_profile_without_authorization(self):
        """Попытка редактирования профиля без авторизации."""
        response = self.client.get(reverse('profile_edit'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile_edit')}")
