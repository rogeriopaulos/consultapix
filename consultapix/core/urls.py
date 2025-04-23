from django.urls import path

from consultapix.core.views import AboutView
from consultapix.core.views import HomeView

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sobre/", AboutView.as_view(), name="about"),
]
