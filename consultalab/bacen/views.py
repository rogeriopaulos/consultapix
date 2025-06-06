import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import View

from consultalab.bacen.forms import RequisicaoBacenForm
from consultalab.bacen.models import RequisicaoBacen
from consultalab.bacen.report import PixReportGenerator
from consultalab.bacen.tasks import request_bacen_pix

logger = logging.getLogger(__name__)


class CPFCNPJFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = RequisicaoBacenForm(initial={"tipo_requisicao": "1"})
        return render(
            request,
            "bacen/partials/pix_modal.html",
            {"form": form, "tipo_requisicao": "1"},
        )


class ChavePixFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = RequisicaoBacenForm(initial={"tipo_requisicao": "2"})
        return render(
            request,
            "bacen/partials/pix_modal.html",
            {"form": form, "tipo_requisicao": "2"},
        )


class RequisicaoBacenCreateView(LoginRequiredMixin, CreateView):
    model = RequisicaoBacen
    form_class = RequisicaoBacenForm
    template_name = "pages/home.html"
    success_url = reverse_lazy("core:home")
    success_message = "Requisição Bacen criada com sucesso!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        requisicoes = RequisicaoBacen.objects.filter(user=self.request.user).order_by(
            "-created",
        )
        response.context_data["requisicoes"] = requisicoes
        response.context_data["messages_toast"] = form.errors["__all__"]
        return response


class ProcessarRequisicaoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        requisicao_id = kwargs.get("requisicao_id")
        requisicao = RequisicaoBacen.objects.get(id=requisicao_id)

        task = request_bacen_pix.delay(requisicao.id)
        requisicao.task_id = task.id
        requisicao.processada = True
        requisicao.save()

        return render(
            request,
            "bacen/partials/requisicao_row.html",
            {"requisicao": requisicao},
        )


class RequisicaoBacenStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        requisicao_id = kwargs.get("requisicao_id")
        requisicao = RequisicaoBacen.objects.get(id=requisicao_id)

        if requisicao.get_status()["finished"]:
            response = render(
                request,
                "bacen/partials/requisicao_row_status.html",
                {"requisicao": requisicao},
            )
            response.status_code = 286
            return response

        return render(
            request,
            "bacen/partials/requisicao_row_status.html",
            {"requisicao": requisicao},
        )


class RequisicaoBacenDetailView(LoginRequiredMixin, DetailView):
    model = RequisicaoBacen
    template_name = "bacen/partials/requisicao_bacen_detail.html"
    context_object_name = "requisicao"

    def get_queryset(self):
        return RequisicaoBacen.objects.prefetch_related("chaves_pix").filter(
            user=self.request.user,
        )


class RequisicaoBacenPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        requisicao_id = kwargs.get("requisicao_id")
        requisicao = RequisicaoBacen.objects.get(id=requisicao_id)

        report_generator = PixReportGenerator()
        data = requisicao.to_dict()
        buffer = report_generator.generate_report(
            data["requisicao_data"],
            data["chaves_pix"],
        )

        return FileResponse(buffer, as_attachment=True, filename="requisicao_bacen.pdf")


class RequisicaoBacenDeleteView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        requisicao_id = kwargs.get("requisicao_id")
        response = render(
            request,
            "bacen/partials/empty_content.html",
            {"requisicao": None},
        )
        has_error = False

        try:
            requisicao = RequisicaoBacen.objects.get(id=requisicao_id)
            if requisicao.user == request.user:
                requisicao.delete()
                response.status_code = 200
                return response
        except RequisicaoBacen.DoesNotExist:
            logger.exception(
                "Requisição Bacen não encontrada ou não pertence ao usuário.",
            )
            has_error = True

        if has_error:
            response["HX-Trigger"] = (
                '{"showMessage": "Ocorreu um erro ao tentar excluir a requisição."}'
            )
            response.status_code = 400
        return response
