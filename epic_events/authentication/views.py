from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from authentication.serializer import TeamSerializer
from authentication.models import RoleModel


class TeamView(ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def update(self, request, pk):
        team_object = self.get_object()
        validated_data = request.data.copy()

        team_object.password = validated_data.get('password', team_object.password)
        team_object.username = validated_data.get('username', team_object.username)
        team_object.first_name = validated_data.get('first_name', team_object.first_name)
        team_object.last_name = validated_data.get('last_name', team_object.last_name)
        if not RoleModel.objects.filter(id=int(validated_data["role"])):
            raise serializers.ValidationError("role is not valid")

        role_instance = RoleModel.objects.get(id=int(validated_data["role"]))
        team_object.role = role_instance

        team_object.save()
        serialiser = self.serializer_class(team_object)
        return Response(serialiser.data)
