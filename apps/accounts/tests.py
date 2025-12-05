from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.data_user = {
            "username": "testuser123",
            "email": "test@example.com",
            "phone_number": "9123456789",
            "bi": "1234567HO123",
            "address": "Luanda, Angola",
            "city": "Luanda",
            "country": "Angola",
        }
    
    def test_create_user(self):
        user = User.objects.create_user(**self.data_user)
        self.assertEqual(user.username, "testuser123")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.phone_number, "9123456789")
        self.assertEqual(user.bi, "1234567HO123")
        self.assertEqual(user.address, "Luanda, Angola")
        self.assertEqual(user.city, "Luanda")
        self.assertEqual(user.country, "Angola")
