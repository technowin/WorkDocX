from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

# Create your views here.

class MapsView(TemplateView):
    pass

maps_google_view = MapsView.as_view(template_name="bootstrap/maps/google.html")
maps_vector_view = MapsView.as_view(template_name="bootstrap/maps/vector.html")
