from rest_framework import status
from rest_framework.test import APIClient

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
