"""
URL configuration for epic_events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from authentication.views import TeamView
from app_clients_contract_event.views import ClientView, ContractView, EventView


router = routers.SimpleRouter()

router.register('team', TeamView, basename='team')
router.register('client', ClientView, basename='client')

contract_router = routers.NestedDefaultRouter(router, 'client', lookup='client')
contract_router.register('contract', ContractView, basename='contract')

event_router = routers.NestedDefaultRouter(contract_router, 'contract', lookup='contract')
event_router.register('event', EventView, basename='event')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='obtain_tokens'),    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include(router.urls)),
    path('api/', include(contract_router.urls)),
    path('api/', include(event_router.urls)),
]
