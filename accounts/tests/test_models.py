from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from blog import models


def sample_user():
    """create a sample superuser"""
    email = "psg@gmail.com"
    password = "mysecretpassword"
    return get_user_model().objects.create_superuser(
        email=email,
        password=password)


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """ Test to validate a user is created with a email successfully."""
        email = "psg@mine.com"
        password = "Testpass123"
        phone = "9802051714"
        name = "paritosh sharma ghimire"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            phone_number=phone,
            name=name)

        self.assertEqual(user.phone_number, phone)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        user.full_clean()
        self.assertTrue(ValidationError, user.full_clean)

    def test_user_email_normalize(self):
        """Test to validate email of new user is normalized"""

        email = "pPsg@GMAIL.COM"
        password = "Testpassword123"
        phone_number = "9802051714"
        name = "hello world"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            name=name)
        email_split = email.split('@')

        self.assertEqual(
            user.email,
            '{}@{}'.format(
                email_split[0],
                email_split[1].lower()))

    def test_user_invalid_email(self):
        """Test to validate user with no email"""
        with self.assertRaises(ValueError):
            # Anything inside this with statement should raise Value error
            # if not this test fails.
            get_user_model().objects.create_user(
                email=None,
                password="testpass123",
                phone_number="9802051714",
                name="paritosh ghimire")

    def test_create_new_superuser(self):
        """Test to validate a superuser is created successfully"""
        user = get_user_model().objects.create_superuser(
            email="psg@mine.com",
            password="testpass123",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_new_staffuser(self):
        """Test to validate a staff user is created successfully"""

        user = get_user_model().objects.create_staff(
            email="mine@mine.com",
            password="nepal123",
        )
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)