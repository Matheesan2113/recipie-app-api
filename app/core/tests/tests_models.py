from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_ceate_user_with_email_successful(self):
        """test  creating new user with email is successful"""
        # verify user, email and pass is correct
        email = "mathee25@hotmail.com"
        password = '12fdfb345'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        #Check pass word needs checking encryypted which means checking to see if true if correct
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
        """ test to see if email for new user is ormalized to lowercase"""
        email = 'test@JBKBBLJNK.COM'
        user = get_user_model().objects.create_user(email, 'test12')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        # Anything ran in with should raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superUser(self):
        """test to see if superuser is created with super user"""
        user = get_user_model().objects.create_superuser(
            'test@dfsdf.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)