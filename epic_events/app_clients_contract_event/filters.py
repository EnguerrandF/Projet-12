from django_filters import rest_framework as filters

from app_clients_contract_event.models import ClientModel


class ClientFilter(filters.FilterSet):
    email = filters.NumberFilter(field_name="email", lookup_expr='icontains')
    compagny_name = filters.NumberFilter(field_name="compagny_name", lookup_expr='icontains')

    class Meta:
        model = ClientModel
        fields = ["email", "compagny_name"]
