from rest_framework import serializers
from authentication.models import TeamModel, RoleModel


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamModel
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = TeamModel.objects.create_user(**validated_data)
        return user

    def validate_role(self, value):
        if not RoleModel.objects.filter(id=value.id):
            raise serializers.ValidationError("role is not valid")
        return RoleModel.objects.get(id=value.id)
