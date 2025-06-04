import django_filters
from django.db.models import Q
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
    busca = django_filters.CharFilter(
        label="",
        method="filter_busca",
        widget=TextInput(
            attrs={
                "class": "form-control form-control-sm ms-5",
            },
        ),
    )

    class Meta:
        model = RequisicaoBacen
        fields = ["created", "busca"]

    def filter_busca(self, queryset, name, value):
        return queryset.filter(
            Q(termo_busca__icontains=value) | Q(motivo__icontains=value),
        )
