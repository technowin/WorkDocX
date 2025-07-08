from django.urls import path

from .views import (
maps_google_view,
maps_vector_view,
)

app_name = "maps"
urlpatterns = [
    path("google", view=maps_google_view,name="google"),
    path("vector", view=maps_vector_view, name="vector"),
]
