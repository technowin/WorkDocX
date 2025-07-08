from django.urls import path

from .views import (
icons_remix_view,
icons_material_view ,
icons_unicons_view ,
icons_lucide_view

)

app_name = "icons"
urlpatterns = [
    path("remix", view=icons_remix_view, name="remix"),
    path("material", view=icons_material_view,name="material"),
    path("unicons", view=icons_unicons_view,name="unicons"),
    path("lucide", view=icons_lucide_view,name="lucide"),
   
]
