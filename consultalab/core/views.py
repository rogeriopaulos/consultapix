from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from consultalab.bacen.filters import RequisicaoBacenFilter
from consultalab.bacen.forms import RequisicaoBacenFilterFormHelper
from consultalab.bacen.models import RequisicaoBacen


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View for the home page.
    """

    template_name = "pages/home.html"
    page_size = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = RequisicaoBacen.objects.filter(user=self.request.user).order_by("-created")
        requisicao_filter = RequisicaoBacenFilter(self.request.GET, queryset=qs)

        requisicao_filter.form.helper = RequisicaoBacenFilterFormHelper()

        paginator = Paginator(requisicao_filter.qs, self.page_size)
        page_number = self.request.GET.get("page")
        try:
            paginated_objects = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_objects = paginator.page(1)
        except EmptyPage:
            paginated_objects = paginator.page(paginator.num_pages)

        context["requisicoes_filter"] = requisicao_filter
        context["requisicoes"] = paginated_objects

        return context


class AboutView(LoginRequiredMixin, TemplateView):
    """
    View for the about page.
    """

    template_name = "pages/about.html"
