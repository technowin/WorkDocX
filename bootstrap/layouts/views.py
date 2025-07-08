from django.views.generic.base import TemplateView


class LayoutsView(TemplateView):
    pass


layouts_vertical_view = LayoutsView.as_view(template_name="bootstrap/layouts/vertical.html")
layouts_horizontal_view = LayoutsView.as_view(template_name="bootstrap/layouts/horizontal.html")
layouts_detached_view = LayoutsView.as_view(template_name="bootstrap/layouts/detached.html")
layouts_full_view = LayoutsView.as_view(template_name="bootstrap/layouts/full.html")
layouts_fullscreen_view = LayoutsView.as_view(template_name="bootstrap/layouts/fullscreen.html")
layouts_hover_view = LayoutsView.as_view(template_name="bootstrap/layouts/hover.html")
layouts_compact_view = LayoutsView.as_view(template_name="bootstrap/layouts/compact.html")
layouts_icon_view = LayoutsView.as_view(template_name="bootstrap/layouts/icon-view.html")
