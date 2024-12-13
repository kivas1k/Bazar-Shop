from unittest.mock import patch, MagicMock
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarshop.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from main.models import MainCategory
from django.core.exceptions import ValidationError


class MainCategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        with patch('django.contrib.auth.models.User.objects.create_superuser') as mock_create_superuser:
            mock_create_superuser.return_value = MagicMock(username='admin')
            cls.admin_user = User.objects.create_superuser(username='admin', password='admin123')

    def test_create_main_category_with_valid_data(self):
        """Тестирование успешного создания категории с валидными данными."""
        category = MainCategory(
            custom_id='unique_id',
            name='Test Category',
            description='Test description'
        )
        category.save()

        saved_category = MainCategory.objects.filter(custom_id='unique_id').first()
        self.assertIsNotNone(saved_category)
        self.assertEqual(saved_category.name, 'Test Category')
        self.assertEqual(saved_category.description, 'Test description')

    def test_create_main_category_with_existing_custom_id(self):
        """Тестирование создания категории с существующим custom_id."""
        MainCategory.objects.create(
            custom_id='duplicat1',
            name='Category 1',
            description='Description 1'
        )
        category = MainCategory(
            custom_id='duplicat1',
            name='Category 2',
            description='Description 2'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_create_main_category_with_empty_custom_id(self):
        """Тестирование создания категории с пустым custom_id."""
        category = MainCategory(
            custom_id='',
            name='Category',
            description='Description'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_edit_main_category(self):
        """Тестирование успешного редактирования категории."""
        category = MainCategory.objects.create(
            custom_id='edit_id',
            name='Old Name',
            description='Old Description'
        )
        category.name = 'New Name'
        category.description = 'New Description'
        category.save()

        updated_category = MainCategory.objects.get(custom_id='edit_id')
        self.assertEqual(updated_category.name, 'New Name')
        self.assertEqual(updated_category.description, 'New Description')

    @patch('main.models.MainCategory.delete')
    def test_successful_delete_main_category(self, mock_delete):
        """Тестирование успешного удаления категории."""
        category = MainCategory.objects.create(
            custom_id='unique_id',
            name='Test Category',
            description='Test description'
        )
        category_id = category.id
        category.delete()


        mock_delete.assert_called_once()

    def test_name_field_length(self):
        """Тестирование минимальной и максимальной длины поля name."""
        short_name = ''
        category_min = MainCategory(
            custom_id='short_name_id',
            name=short_name,
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_min.full_clean()

        long_name = 'a' * 256
        category_max = MainCategory(
            custom_id='long_name_id',
            name=long_name,
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_max.full_clean()

    def test_custom_id_field_length(self):
        """Тестирование минимальной и максимальной длины поля custom_id."""
        short_custom_id = ''
        category_min = MainCategory(
            custom_id=short_custom_id,
            name='Test Category',
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_min.full_clean()

        long_custom_id = 'a' * 256
        category_max = MainCategory(
            custom_id=long_custom_id,
            name='Test Category',
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_max.full_clean()

    def test_create_category_without_required_fields(self):
        """Тестирование создания категории без обязательных полей."""
        category_missing_custom_id = MainCategory(
            custom_id=None,
            name='Test Category',
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_missing_custom_id.full_clean()

        category_missing_name = MainCategory(
            custom_id='unique_id',
            name=None,
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_missing_name.full_clean()

        category_empty_name = MainCategory(
            custom_id='unique_id',
            name='',
            description='Test description'
        )
        with self.assertRaises(ValidationError):
            category_empty_name.full_clean()

    def test_update_category_after_edit(self):
        """Тестирование обновления категории после редактирования."""
        category = MainCategory.objects.create(
            custom_id='unique_id',
            name='Old Name',
            description='Old Description'
        )
        category.name = 'Updated Name'
        category.description = 'Updated Description'
        category.save()

        updated_category = MainCategory.objects.get(id=category.id)
        self.assertEqual(updated_category.name, 'Updated Name')
        self.assertEqual(updated_category.description, 'Updated Description')
        self.assertNotEqual(updated_category.name, 'Old Name')
        self.assertNotEqual(updated_category.description, 'Old Description')
