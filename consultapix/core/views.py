from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from consultapix.bacen.models import RequisicaoBacen


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View for the home page.
    """

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = RequisicaoBacen.objects.filter(user=self.request.user)
        context["requisicoes"] = qs.order_by("-created")
        return context


class AboutView(LoginRequiredMixin, TemplateView):
    """
    View for the about page.
    """

    template_name = "pages/about.html"
