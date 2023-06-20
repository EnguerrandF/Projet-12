from rest_framework.permissions import BasePermission
from rest_framework import permissions

from app_clients_contract_event.models import ClientModel, ContractModel, EventModel
from authentication.models import TeamModel, RoleModel


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            if view.kwargs.get('pk'):
                pk = view.kwargs.get('pk')
                if request.user.role.role == 'commercial':
                    if ClientModel.objects.filter(sales_contact=request.user, id=pk):
                        return True
                elif request.user.role.role == 'gestion':
                    return True
                elif request.user.role.role == 'support':
                    if ClientModel.objects.filter(contractmodel__eventmodel__support_contact=request.user,
                                                  id=pk).distinct():
                        return True
            else:
                if request.user.role.role in ["commercial", "gestion", "support"]:
                    return True
        elif request.method in ['POST']:
            if request.user.role.role in ["commercial", "gestion"]:
                return True
        elif request.method in ['PUT']:
            if request.user.role.role == "commercial":
                pk = view.kwargs.get('pk')
                if ClientModel.objects.filter(sales_contact=request.user, id=pk):
                    return True
            elif request.user.role.role == 'gestion':
                return True


class ContractPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.role.role in ['commercial', 'gestion']:
                return True
        elif request.method == 'GET':
            if view.kwargs.get('pk'):
                pk = view.kwargs.get('pk')
                client_pk = view.kwargs.get('client_pk')
                if request.user.role.role == 'commercial':
                    if ContractModel.objects.filter(id_client=client_pk, id=pk):
                        return True
                elif request.user.role.role == 'gestion':
                    return True
                elif request.user.role.role == 'support':
                    if ContractModel.objects.filter(eventmodel__support_contact=request.user,
                                                    id=pk).distinct():
                        return True
            elif request.user.role.role in ["commercial", "gestion", "support"]:
                return True
        elif request.method == 'PUT':
            if request.user.role.role in ['gestion', 'commercial']:
                return True


class EventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.method == 'GET':
                pass
        else:
            if request.method == 'POST':
                client_pk = view.kwargs["client_pk"]
                contract_pk = view.kwargs["contract_pk"]
                if ((client_authorization(request, client_pk) and
                     contract_authorization(request, client_pk, contract_pk)) and
                   (commercial_authorization(request) or gestion_authorization(request))):
                    return True
            elif request.method == 'PUT':
                pass


def commercial_authorization(request):
    if request.user.role == RoleModel.objects.get(role="commercial"):
        return True
    return False


def support_authorization(request):
    if request.user.role == RoleModel.objects.get(role="support"):
        return True
    return False


def gestion_authorization(request):
    if request.user.role == RoleModel.objects.get(role="gestion"):
        return True
    return False


def client_authorization(request, client_pk):
    if request.user.id == ClientModel.objects.get(id=client_pk).sales_contact.id:
        return True
    return False


def contract_authorization(request, client_pk, contract_pk):
    if ContractModel.objects.get(id=contract_pk).id_client.id == int(client_pk):
        return True
    return False
