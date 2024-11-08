"""
Tests for the Django admin notifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """ Tests for Django admin. """

    # setUp for the tests on admin
    def setUp(self):
        """ Create user and client. """

        # Create the cliente to make requests
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        # force auth for this user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password567',
            first_name='Test User'
        )

    def test_users_list(self):
        """ Test that users are listed on page. """

        # Get the url to get the changelist for the django admin
        # Documentation: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls  # noqa
        url = reverse('admin:core_user_changelist')
        # Make a http request to the url with the auth user
        res = self.client.get(url)

        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """ Test the edit user page works. """

        # Get the url for the edit page in the admin panel with the id of the user we wanna update  # noqa
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Edit page load correctly
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test the create user page works. """

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
