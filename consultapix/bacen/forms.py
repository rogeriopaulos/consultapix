from django import forms

from consultapix.bacen.models import RequisicaoBacen


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
