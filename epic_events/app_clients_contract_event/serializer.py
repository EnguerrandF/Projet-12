from rest_framework import serializers

from app_clients_contract_event.models import ClientModel, ContractModel, EventModel


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['id', 'compagny_name']


class ClientSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'compagny_name', 'sales_contact']

    def validate(self, value):
        if len(str(value["phone"])) == 10 or len(str(value["mobile"])) == 10:
            raise serializers.ValidationError("number is not valid")
        return value


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractModel
        fields = ["id", "id_client"]


class ContractSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = ContractModel
        fields = ["id", "payment_due", "amount", "id_client"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = ["id", "id_contract"]


class EventSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = ["id", "event_date", "attenteeds", "note", "status",  "support_contact", "id_contract"]
