from http import HTTPStatus

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from consultapix.core.views import HomeView
from consultapix.users.models import User
from consultapix.users.tests.factories import UserFactory

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
