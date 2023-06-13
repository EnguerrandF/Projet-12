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
from authentication.models import TeamModel


class ClientView(ModelViewSet):
    serializer_class = ClientSerializer
    detail_serializer = ClientSerializerDetail
    permission_classes = [IsAuthenticated]
    queryset = ClientModel
    pagination_class = PageNumberPagination
    # filterset_class = ClientFilter

    def create(self, request,):
        serializer = self.detail_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request):
        email = request.query_params.get('email')
        compagny_name = request.query_params.get('compagny_name')

        if email:
            queryset = self.queryset.objects.filter(email=email)
        elif compagny_name:
            queryset = self.queryset.objects.filter(compagny_name=compagny_name)
        else:
            queryset = self.queryset.objects.all()

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.detail_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        client_object = self.get_object()
        validated_data = request.data.copy()

        client_object.first_name = validated_data.get('first_name', client_object.first_name)
        client_object.last_name = validated_data.get('last_name', client_object.last_name)
        client_object.email = validated_data.get('email', client_object.email)
        client_object.phone = validated_data.get('phone', client_object.phone)
        client_object.mobile = validated_data.get('mobile', client_object.mobile)
        client_object.compagny_name = validated_data.get('compagny_name', client_object.compagny_name)

        if not TeamModel.objects.filter(id=int(validated_data["sales_contact"])):
            raise serializers.ValidationError("id is not valid")

        sales_contact_instance = TeamModel.objects.get(id=int(validated_data["sales_contact"]))
        client_object.sales_contact = sales_contact_instance

        client_object.save()
        serialiser = self.detail_serializer(client_object)
        return Response(serialiser.data)


class ContractView(ModelViewSet):
    serializer_class = ContractSerializer
    detail_serializer = ContractSerializerDetail
    permission_classes = [IsAuthenticated]
    queryset = ContractModel
    pagination_class = PageNumberPagination
    # filterset_class = 

    def create(self, request, client_pk):
        data = request.data.copy()
        data['id_client'] = int(client_pk)
        serializer = self.detail_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, client_pk):
        payment_due = request.query_params.get('payment_due')
        amount = request.query_params.get('amount')

        if payment_due:
            queryset = self.queryset.objects.filter(payment_due=payment_due)
        elif amount:
            queryset = self.queryset.objects.filter(amount=amount)
        else:
            queryset = self.queryset.objects.filter(id_client=client_pk)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, client_pk):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.detail_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk, client_pk):
        contract_object = self.get_object()
        validated_data = request.data.copy()

        contract_object.payment_due = validated_data.get('payment_due', contract_object.payment_due)
        contract_object.amount = validated_data.get('amount', contract_object.amount)

        contract_object.save()
        serialiser = self.detail_serializer(contract_object)
        return Response(serialiser.data)


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    detail_serializer = EventSerializerDetail
    permission_classes = [IsAuthenticated]
    queryset = EventModel
    pagination_class = PageNumberPagination
    # filterset_class =

    def create(self, request, client_pk, contract_pk):
        data = request.data.copy()
        data['id_contract'] = int(contract_pk)
        serializer = self.detail_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, client_pk, contract_pk):
        event_date = request.query_params.get('event_date')

        if event_date:
            queryset = self.queryset.objects.filter(event_date=event_date)
        else:
            queryset = self.queryset.objects.filter(id_contract=contract_pk)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, client_pk, contract_pk, pk):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.detail_serializer(user)
        return Response(serializer.data)

    def update(self, request, client_pk, contract_pk, pk):
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
        print(event_object, "oOOOOOOOOOOOOOOOOOOO")
        event_object.status = status_instance
        event_object.support_contact = support_contact_instance
        event_object.save()
        serialiser = self.detail_serializer(event_object)
        return Response(serialiser.data)
