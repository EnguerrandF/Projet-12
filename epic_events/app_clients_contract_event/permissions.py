from rest_framework.permissions import BasePermission

from app_clients_contract_event.models import ClientModel, ContractModel


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            if request.user.role.role in ["commercial", "gestion", "support"]:
                return True
        elif request.method in ['POST', 'PUT']:
            if request.user.role.role in ["commercial", "gestion"]:
                return True
        return False


class ContractPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            if (request.user.role.role == 'commercial' and
                    ClientModel.objects.filter(sales_contact=request.user,
                                               id=request.data['id_client'])):
                return True
            elif request.user.role.role == 'gestion':
                return True
        elif request.method == 'GET':
            if request.user.role.role in ['commercial', 'support', 'gestion']:
                return True


class EventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if (request.user.role.role in ['commercial'] and
                    ContractModel.objects.filter(id_client__sales_contact=request.user,
                                                 id=request.data["id_contract"])):
                return True
            elif request.user.role.role == 'gestion':
                return True
        elif request.method == 'GET':
            if request.user.role.role in ["support", 'gestion']:
                return True
        elif request.method == 'PUT':
            if (request.user.role.role == 'support' and
                    view.get_object().status.status != 'finished'):
                return True
            elif request.user.role.role == 'gestion':
                return True
