from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from authentication.serializer import TeamSerializer
from authentication.models import TeamModel
from authentication.permissions import TeamPermission


class TeamView(ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]
    pagination_class = PageNumberPagination
    queryset = TeamModel.objects.all()

    def update(self, request, pk):
        instance = self.get_object()
        data = request.data.copy()
        instance.set_password(data['password'])
        data['password'] = instance.password
        serializer = self.get_serializer(instance, data=data, )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
