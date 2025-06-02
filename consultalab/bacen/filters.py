import django_filters
from django.forms import TextInput

from consultalab.bacen.models import RequisicaoBacen


class RequisicaoBacenFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={
                "placeholder": "YYYY/MM/DD",
                "type": "date",
                "class": "form-control form-control-sm",
            },
        ),
        label="",
    )
    termo_busca = django_filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control form-control-sm ms-5",
            },
        ),
    )

    class Meta:
        model = RequisicaoBacen
        fields = ["created", "termo_busca"]
