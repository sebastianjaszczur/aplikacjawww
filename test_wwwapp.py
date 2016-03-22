from django.test import TestCase, Client


class AnimalTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_admin_page(self):
        """Tests if admin page works"""
        response = self.client.get('/admin', follow=True)
        self.assertContains(response, "Django admin", status_code=200)
