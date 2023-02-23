from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from model_bakery import baker
from store.models import Collection
import pytest


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        res = client.post('/store/collections/', {'title': 'a'})

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_non_admin_returns_403(self):
        client = APIClient()
        # to authenticate the user
        client.force_authenticate(user={})
        res = client.post('/store/collections/', {'title': 'a'})

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        # *to authenticate the user as ADMIN
        client.force_authenticate(user=User(is_staff=True))
        res = client.post('/store/collections/', {'title': ''})

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data['title'] is not None

    def test_if_data_is_valid_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        res = client.post('/store/collections/', {'title': 'a'})

        assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetreiveCollection:

    def test_if_collection_exists_returns_200(self):
        # Arrange ->
        # *create a collection first
        collection = baker.make(Collection)

        client = APIClient()
        res = client.get(f'/store/collections/{collection.id}/')

        assert res.status_code == status.HTTP_200_OK
        assert res.data['id'] == collection.id
