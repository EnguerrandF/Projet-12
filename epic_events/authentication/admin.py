from django.contrib import admin

from authentication.models import TeamModel, RoleModel


class TeamModelAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "role")


class RoleModelAdmin(admin.ModelAdmin):
    list_display = ("id", "role")


admin.site.register(TeamModel, TeamModelAdmin)
admin.site.register(RoleModel, RoleModelAdmin)
