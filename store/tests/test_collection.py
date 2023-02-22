from rest_framework import status
from rest_framework.test import APIClient

import pytest


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous(self):
        client = APIClient()
        res = client.post('/store/collections/', {'title': 'a'})

        assert res.status_code == status.HTTP_401_UNAUTHORIZED
