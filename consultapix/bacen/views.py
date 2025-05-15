from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import View

from consultapix.bacen.forms import RequisicaoBacenForm
from consultapix.bacen.models import RequisicaoBacen
from consultapix.bacen.tasks import request_pix_by_cpfcnpj


class CPFCNPJFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = RequisicaoBacenForm(initial={"tipo_requisicao": "1"})
        return render(request, "bacen/partials/pix_modal.html", {"form": form})


class ChavePixFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = RequisicaoBacenForm(initial={"tipo_requisicao": "2"})
        return render(request, "bacen/partials/pix_modal.html", {"form": form})


class RequisicaoBacenCreateView(LoginRequiredMixin, CreateView):
    model = RequisicaoBacen
    form_class = RequisicaoBacenForm
    template_name = "bacen/partials/pix_modal.html"
    success_url = reverse_lazy("core:home")
    success_message = "Requisição Bacen criada com sucesso!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProcessarRequisicaoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        requisicao_id = kwargs.get("requisicao_id")
        requisicao = RequisicaoBacen.objects.get(id=requisicao_id)

        task = request_pix_by_cpfcnpj.delay(requisicao.termo_busca)
        requisicao.task_id = task.id
        requisicao.processada = True
        requisicao.save()

        return render(
            request,
            "bacen/partials/requisicao_row.html",
            {"requisicao": requisicao},
        )
