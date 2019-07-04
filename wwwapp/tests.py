from django.contrib.auth.models import User
from django.test import TestCase


class MainViewsTestCase(TestCase):
    fixtures = ['simpletestdata.json']
    
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(r'Strona główna' in resp.content.decode())
        self.assertTrue(r'Artykuły' in resp.content.decode())
        self.assertTrue(r'Warsztaty' in resp.content.decode())
        
        self.assertFalse(r'Wybierz metodę logowania' in resp.content.decode())
        
    def test_login(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(r'Wybierz metodę logowania' in resp.content.decode())
        self.assertTrue(r'Strona główna' in resp.content.decode())
        self.assertTrue(r'Artykuły' in resp.content.decode())
        self.assertTrue(r'Warsztaty' in resp.content.decode())
    
    def test_emails(self):
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.client.login(username="admin", password="admin")
        resp = self.client.get('/emails/')
        self.client.logout()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('[{"workshopname": "WarsztatyKow", "email": "jan@kowalski.com", "name": "Jan Kowalski-\\u0104\\u0119"}]' in resp.content.decode())
    
    def test_add_workshops(self):
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.client.login(username="admin", password="admin")
        resp = self.client.get('/addWorkshop/')
        self.client.logout()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(r'Zapisz' in resp.content.decode())
        self.assertTrue(r'</form>' in resp.content.decode())
    
    def test_program(self):
        resp = self.client.get('/2016/program/')
        self.client.logout()
        # self.assertEqual(resp.status_code, 200)
        # self.assertTrue(r'Program WWW' in resp.content.decode())
        # self.assertTrue(r'WarsztatyKow' in resp.content.decode())        

    def test_email_filter(self):
        resp = self.client.get('/filterEmails/2016/all/')
        self.assertEqual(resp.status_code, 302)

        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.client.login(username="admin", password="admin")
        resp = self.client.get('/filterEmails/2016/all/')
        self.assertTrue('jan@kowalski.com' in resp.content.decode())
