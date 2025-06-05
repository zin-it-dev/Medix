from django.test import TestCase

from ..models import Category

class CategoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="This is a test!")

    def test_model_content(self):
        self.assertEqual(self.category.name, "This is a test!")

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)