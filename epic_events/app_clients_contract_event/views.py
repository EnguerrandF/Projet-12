from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from app_clients_contract_event.serializer import ClientSerializer, ClientSerializerDetail, ContractSerializer,\
    ContractSerializerDetail, EventSerializer, EventSerializerDetail
from app_clients_contract_event.models import ClientModel, ContractModel, EventModel, StatusModel
from app_clients_contract_event.filters import ClientFilter
from app_clients_contract_event.permissions import ClientPermission, ContractPermission, EventPermission
from authentication.models import TeamModel, RoleModel


class ClientView(ModelViewSet):
    serializer_class = ClientSerializerDetail
    limit_serializer = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    queryset = ClientModel
    pagination_class = PageNumberPagination

    def list(self, request):
        if request.user.role.role in ['commercial']:
            queryset_data = self.queryset.objects.filter(sales_contact=request.user)
        elif request.user.role.role in ['gestion']:
            queryset_data = self.queryset.objects.all()
        elif request.user.role.role in ['support']:
            queryset_data = self.queryset.objects.filter(
                contractmodel__eventmodel__support_contact=request.user).distinct()
        else:
            queryset_data = []

        serializer = self.limit_serializer(queryset_data, many=True)
        return Response(serializer.data)


class ContractView(ModelViewSet):
    serializer_class = ContractSerializerDetail
    limit_serializer = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    queryset = ContractModel
    pagination_class = PageNumberPagination

    def dispatch(self, request, *args, **kwargs):
        """ Check the rights of the connected user on the Customer with permission from ClientView """
        parent_view = ClientView.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"pk": kwargs["client_pk"]}
        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, client_pk):
        data = request.data.copy()
        data['id_client'] = int(client_pk)
        serializer = self.detail_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, client_pk):
        if request.user.role.role in ['gestion', 'commercial']:
            queryset = self.queryset.objects.filter(id_client=client_pk)
        elif request.user.role.role == 'support':
            queryset = self.queryset.objects.filter(eventmodel__support_contact=request.user)

        serializer = self.limit_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk, client_pk):
        instance = self.get_object()
        data = request.data.copy()
        data['id_client'] = int(client_pk)

        serializer = self.serializer_class(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    detail_serializer = EventSerializerDetail
    permission_classes = [IsAuthenticated, EventPermission]
    queryset = EventModel
    pagination_class = PageNumberPagination
    # filterset_class =

    def create(self, request, client_pk, contract_pk):
        self.check_object_permissions(self.request, self.queryset)
        data = request.data.copy()
        data['id_contract'] = int(contract_pk)
        serializer = self.detail_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, client_pk, contract_pk):
        self.check_object_permissions(self.request, self.queryset)
        event_date = request.query_params.get('event_date')

        if event_date:
            queryset = self.queryset.objects.filter(event_date=event_date)
        else:
            queryset = self.queryset.objects.filter(id_contract=contract_pk)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, client_pk, contract_pk, pk):
        self.check_object_permissions(self.request, self.queryset)
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.detail_serializer(user)
        return Response(serializer.data)

    def update(self, request, client_pk, contract_pk, pk):
        self.check_object_permissions(self.request, self.queryset)
        event_object = self.get_object()
        validated_data = request.data.copy()

        event_object.event_date = validated_data.get('event_date', event_object.event_date)
        event_object.attenteeds = validated_data.get('attenteeds', event_object.attenteeds)
        event_object.note = validated_data.get('note', event_object.note)

        if (not StatusModel.objects.filter(id=int(validated_data["status"])) or
                not TeamModel.objects.filter(id=int(validated_data["support_contact"]))):
            raise serializers.ValidationError("id is not valid")

        status_instance = StatusModel.objects.get(id=int(validated_data["status"]))
        support_contact_instance = TeamModel.objects.get(id=int(validated_data["support_contact"]))

        event_object.status = status_instance
        event_object.support_contact = support_contact_instance
        event_object.save()
        serialiser = self.detail_serializer(event_object)
        return Response(serialiser.data)
