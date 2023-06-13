from django.contrib import admin

from app_clients_contract_event.models import ClientModel, ContractModel, StatusModel, EventModel


class ClientModelAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "compagny_name")


class ContractModelAdmin(admin.ModelAdmin):
    list_display = ("id", "id_client", "payment_due")


class StatusModelAdmin(admin.ModelAdmin):
    list_display = ("id", "status")


class EventModelAdmin(admin.ModelAdmin):
    list_display = ("id", "event_date", "status", "id_contract")


admin.site.register(ClientModel, ClientModelAdmin)
admin.site.register(ContractModel, ContractModelAdmin)
admin.site.register(StatusModel, StatusModelAdmin)
admin.site.register(EventModel, EventModelAdmin)
