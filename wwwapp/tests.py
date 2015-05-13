#-*- coding: utf-8 -*-
from django.test import TestCase 
from django.contrib.auth.models import User


class MainViewsTestCase(TestCase):
    fixtures = ['simpletestdata.json']
    
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(r'Strona główna' in resp.content)
        self.assertTrue(r'Artykuły' in resp.content)
        self.assertTrue(r'Warsztaty' in resp.content)
        
        self.assertFalse(r'Wybierz metodę logowania' in resp.content)
        
    def test_login(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(r'Wybierz metodę logowania' in resp.content)
        self.assertTrue(r'Strona główna' in resp.content)
        self.assertTrue(r'Artykuły' in resp.content)
        self.assertTrue(r'Warsztaty' in resp.content)
    
    def test_emails(self):
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.client.login(username="admin", password="admin")
        resp = self.client.get('/emails/')
        self.client.logout()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(r'[{"workshopname": "WarsztatyKow", "email": "jan@kowalski.com", "name": "Jan Kowalski"}]' in resp.content)
        
