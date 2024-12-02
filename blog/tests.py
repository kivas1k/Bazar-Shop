#django mock доделать

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarshop.settings')
django.setup()

from io import BytesIO
from PIL import Image
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.utils.translation import override
from .models import Post

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarshop.settings')
django.setup()


class BlogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')

        self.post = Post.objects.create(
            custom_id='test-post',
            title='Test Post',
            content='This is a test post.',
            author=self.admin,
        )

    def tearDown(self):
        """Очистка созданных файлов."""
        posts = Post.objects.all()
        for post in posts:
            if post.image and os.path.exists(post.image.path):
                os.remove(post.image.path)

    def create_test_image(self):
        """Создание тестового изображения."""
        image = Image.new('RGB', (1000, 1000), color='blue')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return SimpleUploadedFile('test_image.jpg', buffer.read(), content_type='image/jpeg')

    def test_create_post_as_admin(self):
        """Тест создания поста администратором."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('blog_create'), {
            'custom_id': 'new-post',
            'title': 'New Post',
            'content': 'Content of new post.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(custom_id='new-post').exists())

    def test_create_post_as_non_admin(self):
        """Тест запрета создания поста обычным пользователем."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog_create'), {
            'custom_id': 'user-post',
            'title': 'User Post',
            'content': 'Content by a regular user.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(custom_id='user-post').exists())

    def test_edit_post_as_admin(self):
        """Тест редактирования поста администратором."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('blog_edit', args=[self.post.custom_id]), {
            'custom_id': 'test-post',
            'title': 'Updated Title',
            'content': 'Updated Content.',
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated Content.')

    def test_edit_post_as_non_admin(self):
        """Тест запрета редактирования поста обычным пользователем."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('blog_edit', args=[self.post.custom_id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_post_as_admin(self):
        """Тест удаления поста администратором."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('blog_delete', args=[self.post.custom_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(custom_id='test-post').exists())

    def test_delete_post_as_non_admin(self):
        """Тест запрета удаления поста обычным пользователем."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog_delete', args=[self.post.custom_id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(custom_id='test-post').exists())

    # === Тесты изображений ===

    def test_create_post_with_image(self):
        """Тест создания поста с изображением."""
        self.client.login(username='admin', password='adminpass')
        image = self.create_test_image()
        response = self.client.post(reverse('blog_create'), {
            'custom_id': 'post-with-image',
            'title': 'Post with Image',
            'content': 'Content with image.',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(custom_id='post-with-image')
        self.assertTrue(post.image)

        with Image.open(post.image.path) as img:
            self.assertEqual(img.size, (800, 800))

    def test_delete_post_with_image(self):
        """Тест удаления поста с изображением."""
        self.client.login(username='admin', password='adminpass')
        post = Post.objects.create(
            custom_id='image-post',
            title='Image Post',
            content='Content with image.',
            author=self.admin,
            image=self.create_test_image(),
        )
        image_path = post.image.path

        self.assertTrue(os.path.exists(image_path), "Файл изображения должен существовать до удаления поста.")

        response = self.client.post(reverse('blog_delete', args=[post.custom_id]))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Post.objects.filter(custom_id='image-post').exists(), "Пост должен быть удалён.")
        self.assertFalse(os.path.exists(image_path), "Файл изображения должен быть удалён.")

    # === Проверка граничных значений ===

    def test_custom_id_max_length(self):
        """Тест максимально допустимой длины custom_id."""
        self.client.login(username='admin', password='adminpass')
        custom_id = 'a' * 255
        response = self.client.post(reverse('blog_create'), {
            'custom_id': custom_id,
            'title': 'Valid Title',
            'content': 'Valid Content.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(custom_id=custom_id).exists())

    def test_custom_id_exceeds_max_length(self):
        """Тест превышения максимально допустимой длины custom_id."""
        self.client.login(username='admin', password='adminpass')
        custom_id = 'a' * 256

        with override('en'):
            response = self.client.post(reverse('blog_create'), {
                'custom_id': custom_id,
                'title': 'Too Long Title',
                'content': 'Content.',
            })

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Ensure this value has at most 255 characters (it has 256).')
            self.assertFalse(Post.objects.filter(custom_id=custom_id).exists())

    # === Тесты доступа ===

    def test_anonymous_user_access(self):
        """Тест доступа анонимного пользователя."""
        response = self.client.get(reverse('blog_home'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('blog_post', args=[self.post.custom_id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('blog_create'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('blog_edit', args=[self.post.custom_id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('blog_delete', args=[self.post.custom_id]))
        self.assertEqual(response.status_code, 302)
