from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSitetests(TestCase):

    #  Setup function, test run before every test is run
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='gsf@df.com',
            password='erwf2'
        )
        #  don't have to manually log user in
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@dfdf.com',
            password='dpasswordf3',
            name='test user full name'
        )

    def test_users_listed(self):
        """test users are isted on user page"""
        #  creates url from reverse for page admin, updates automatically based on reverse
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        #  test to see if res(url) has username and email
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        #  admin/core/user anything passed in above, gets passed into the ID
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
