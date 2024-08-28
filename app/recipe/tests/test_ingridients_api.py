"""
Tests for the ingridiemnts API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingridient

from recipe.serializers import IngridientSerializer

INGRIDIENTS_URL = reverse('recipe:ingridient-list')

def detail_url(ingridient_id):
    """Create and return an ingridient detail URL"""
    return reverse('recipe:ingridient-detail', args=[ingridient_id])

def create_user(email='user@example.com', password='testpass123'):
    """Create and return user"""
    return get_user_model().objects.create_user(email=email, password=password)

class PubllicIngridientsApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingridients"""
        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngridientsApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_rerive_ingridients(self):
        """Test retrieving a list of ingridients"""
        Ingridient.objects.create(user=self.user, name='Kale')
        Ingridient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGRIDIENTS_URL)

        ingridients = Ingridient.objects.all().order_by('-name')
        serializer = IngridientSerializer(ingridients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridient_limited_to_user(self):
        """Test list of ingirdients is limited to authenticated user"""
        user2 = create_user(email='user2@example.com')
        Ingridient.objects.create(user=user2, name='Salt')
        ingridient = Ingridient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingridient.name)
        self.assertEqual(res.data[0]['id'], ingridient.id)

    def test_update_ingridient(self):
        """Test updating ingridient"""
        ingridient = Ingridient.objects.create(user=self.user, name='Cilantro')

        payload = {'name': 'Coriander'}
        url = detail_url(ingridient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingridient.refresh_from_db()
        self.assertEqual(ingridient.name, payload['name'])

    def test_delete_ingrdients(self):
        """Test deleting an ingridient"""
        ingridient = Ingridient.objects.create(user=self.user, name='Lettuce')

        url = detail_url(ingridient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingridients = Ingridient.objects.filter(user=self.user)
        self.assertFalse(ingridients.exists())