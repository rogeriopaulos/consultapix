from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View for the home page.
    """

    template_name = "pages/home.html"


class AboutView(LoginRequiredMixin, TemplateView):
    """
    View for the about page.
    """

    template_name = "pages/about.html"
