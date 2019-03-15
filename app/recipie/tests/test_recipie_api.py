from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipie

from recipie.serializers import RecipieSerializer


RECIPIES_URL = reverse('recipie:recipie-list')


#  any additional parm passed in will be passed into a dict called params
def sample_recipie(user, **params):
    """ Create and return sample recipie"""
    defaults = {
        'title': 'sample recipie',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)  #  Updates everything in dict, or creates it with default values

    return Recipie.objects.create(user=user, **defaults)


class PublicRecipiesApiTests(TestCase):
    """ Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ test auth is required """
        res = self.client.get(RECIPIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipiesApiTests(TestCase):
    """ """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipies(self):
        """ retrieve recipies"""
        sample_recipie(user=self.user)
        sample_recipie(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipies = Recipie.objects.all().order_by('-id')
        serializer = RecipieSerializer(recipies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipies_limited_to_user(self):
        """ """
        user2 = get_user_model().objects.create_user(
            'test2@test4.com','pass'
        )
        sample_recipie(user=user2)
        sample_recipie(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipies = Recipie.objects.filter(user=self.user)
        serializer = RecipieSerializer(recipies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)
