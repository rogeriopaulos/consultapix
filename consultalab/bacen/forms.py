from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Column
from crispy_forms.layout import Field
from crispy_forms.layout import Layout
from crispy_forms.layout import Row
from django import forms

from consultalab.bacen.models import RequisicaoBacen


class RequisicaoBacenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo_requisicao"].label = ""
        self.fields["tipo_requisicao"].widget.attrs["type"] = "hidden"
        self.fields["termo_busca"].required = True
        self.fields["motivo"].required = True

    class Meta:
        model = RequisicaoBacen
        fields = [
            "tipo_requisicao",
            "termo_busca",
            "motivo",
        ]
        widgets = {
            "termo_busca": forms.TextInput(attrs={"class": "form-control"}),
            "motivo": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "termo_busca": "Termo de Busca (obrigatório)",
            "motivo": "Motivo (obrigatório)",
        }
        help_texts = {
            "motivo": "BO, IPL, Nº Caso LAB-LD, RIF, Processo Judicial...",
        }

    def clean(self):
        cleaned_data = super().clean()
        termo_busca = cleaned_data.get("termo_busca")
        tipo_requisicao = cleaned_data.get("tipo_requisicao")

        if tipo_requisicao == "1" and not termo_busca.isdigit():
            message = "O termo de busca deve ser um CPF válido."
            raise forms.ValidationError(message)

        return cleaned_data


class RequisicaoBacenFilterFormHelper(FormHelper):
    form_method = "GET"
    layout = Layout(
        Row(
            Column(
                HTML(
                    """
                    <label for="div_id_created" class="form-label">
                        Data de criação
                    </label>
                    """,
                ),
                Field("created"),
            ),
            Column(
                Row(
                    Column(
                        Field(
                            HTML(
                                '<label for="div_id_created" class="form-label ms-5">Pesquisar</label>',  # noqa: E501
                            ),
                            "busca",
                            placeholder="cpf, cnpj, motivo...",
                        ),
                        css_class="col-8",
                    ),
                    Column(
                        HTML(
                            """
                            <button type="button"
                                    class="btn btn-sm btn-outline-primary ms-5 mt-3"
                                    id="filter-button">
                                <i class="bi bi-filter"></i> Filtrar
                            </button>
                            """,
                        ),
                    ),
                    css_class="align-items-center",
                ),
                css_class="ms-5",
            ),
            css_class="d-flex justify-content-between align-items-center",
        ),
    )
