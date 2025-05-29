import django_filters

from consultalab.bacen.models import RequisicaoBacen


class RequisicaoBacenFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'YYYY/MM/DD', 'type': 'date'}),
        label='Data de criação',
        help_text='Filtra as requisições pela data de criação.',
    )

    class Meta:
        model = RequisicaoBacen
        fields = {
            'termo_busca': ['icontains'],
            'motivo': ['icontains']
        }
