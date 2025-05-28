from http import HTTPStatus

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from consultalab.core.views import HomeView
from consultalab.users.models import User
from consultalab.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestHomeView:
    def test_non_authenticated_user(self, user: User, rf: RequestFactory):
        request = rf.get("/")
        request.user = AnonymousUser()
        response = HomeView.as_view()(request, pk=user.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/contas/login/?next=/"

    def test_authenticated_user(self, user: User, rf: RequestFactory):
        request = rf.get("/")
        request.user = UserFactory()
        response = HomeView.as_view()(request, pk=user.pk)

        assert response.status_code == HTTPStatus.OK
