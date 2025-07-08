from django.urls import path

from .views import (
tables_basic_view,
tables_datatable_view,
)

app_name = "tables"
urlpatterns = [
    path("basic", view=tables_basic_view, name="basic"),
    path("datatable", view=tables_datatable_view,name="datatable")
]
