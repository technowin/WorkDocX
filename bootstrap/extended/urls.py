from django.urls import path

from .views import (
extended_dragula_view,
extended_range_slider_view,
extended_ratings_view,
extended_scrollbar_view,
extended_scrollspy_view,
extended_treeview_view

)

app_name = "extended"

urlpatterns = [
    path("dragula", view=extended_dragula_view,name="dragula"),
    path("range-slider", view=extended_range_slider_view,name="range-slider"),
    path("ratings", view=extended_ratings_view,name="ratings"),
    path("scrollbar", view=extended_scrollbar_view,name="scrollbar"),
    path("scrollspy", view=extended_scrollspy_view,name="scrollspy"),
    path("treeview", view=extended_treeview_view,name="treeview"),
   
]
