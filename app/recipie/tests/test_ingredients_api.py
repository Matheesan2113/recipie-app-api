from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipie.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipie:ingredient-list')

class PublicIngredientsApiTests(TestCase):
    """ """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateIngredientsApiTests(TestCase):
    """ """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """ """
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """ test to see if ingredients for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'test1@test2.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Vineagar')
        #   checking later that name of ingredient matches what we pass in
        ingredient = Ingredient.objects.create(user = self.user, name='Timeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """ """
        payload = {'name':'cabbage'}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_valid(self):
        """ """
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
