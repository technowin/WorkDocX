from django.urls import path

from .views import (layouts_vertical_view, layouts_horizontal_view, layouts_detached_view, layouts_full_view,
                    layouts_fullscreen_view,
                    layouts_hover_view, layouts_compact_view, layouts_icon_view)

app_name = "layouts"
urlpatterns = [
    path("vertical", view=layouts_vertical_view, name="vertical"),
    path("horizontal", view=layouts_horizontal_view, name="horizontal"),
    path("detached", view=layouts_detached_view, name="detached"),
    path("full", view=layouts_full_view, name="full"),
    path("fullscreen", view=layouts_fullscreen_view, name="fullscreen"),
    path("hover", view=layouts_hover_view, name="hover"),
    path("compact", view=layouts_compact_view, name="compact"),
    path("icon-view", view=layouts_icon_view, name="icon-view"),
]
