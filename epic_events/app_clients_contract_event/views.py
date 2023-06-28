from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from app_clients_contract_event.serializer import ClientSerializer, ClientSerializerDetail, ContractSerializer,\
    ContractSerializerDetail, EventSerializer, EventSerializerDetail
from app_clients_contract_event.models import ClientModel, ContractModel, EventModel
from app_clients_contract_event.permissions import ClientPermission, ContractPermission, EventPermission


class ClientView(ModelViewSet):
    serializer_class = ClientSerializerDetail
    limit_serializer = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    queryset = ClientModel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('compagny_name', 'email')

    def get_queryset(self):
        if self.request.user.role.role in ['commercial']:
            queryset_data = ClientModel.objects.filter(sales_contact=self.request.user)
        elif self.request.user.role.role in ['gestion']:
            queryset_data = ClientModel.objects.all()
        elif self.request.user.role.role in ['support']:
            queryset_data = ClientModel.objects.filter(
                contractmodel__eventmodel__support_contact=self.request.user).distinct()
        return queryset_data

    def get_serializer_class(self):
        if self.action == 'list':
            return self.limit_serializer
        return super().get_serializer_class()


class ContractView(ModelViewSet):
    serializer_class = ContractSerializerDetail
    limit_serializer = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    queryset = ContractModel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('payment_due', 'amount')

    def get_queryset(self):
        if self.request.user.role.role in ['commercial']:
            queryset_data = ContractModel.objects.filter(id_client__sales_contact=self.request.user)
        elif self.request.user.role.role == 'support':
            queryset_data = ContractModel.objects.filter(eventmodel__support_contact=self.request.user)
        elif self.request.user.role.role == 'gestion':
            queryset_data = self.queryset
        return queryset_data

    def get_serializer_class(self):
        if self.action == 'list':
            return self.limit_serializer
        return super().get_serializer_class()


class EventView(ModelViewSet):
    serializer_class = EventSerializerDetail
    limit_serializer = EventSerializer
    permission_classes = [IsAuthenticated, EventPermission]
    queryset = EventModel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('event_date',)

    def get_queryset(self):
        if self.request.user.role.role == 'gestion':
            queryset_data = self.queryset
        elif self.request.user.role.role == 'support':
            queryset_data = EventModel.objects.filter(support_contact=self.request.user)
        return queryset_data

    def get_serializer_class(self):
        if self.action == 'list':
            return self.limit_serializer
        return super().get_serializer_class()
