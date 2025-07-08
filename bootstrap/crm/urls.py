from django.urls import path

from .views import (crm_projects_view, crm_orders_list_view, crm_clients_view, crm_management_view)

app_name = "crm"
urlpatterns = [
    path("projects", view=crm_projects_view, name="projects"),
    path("orders-list", view=crm_orders_list_view, name="orders-list"),
    path("clients", view=crm_clients_view, name="clients"),
    path("management", view=crm_management_view, name="management")    

]
