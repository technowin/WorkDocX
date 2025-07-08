from django.views.generic import TemplateView

# Create your views here.


class IconsView(TemplateView):
    pass
icons_remix_view = IconsView.as_view(template_name="bootstrap/icons/remix.html")
icons_material_view = IconsView.as_view(template_name="bootstrap/icons/mdi.html")
icons_unicons_view = IconsView.as_view(template_name="bootstrap/icons/unicons.html")
icons_lucide_view = IconsView.as_view(template_name="bootstrap/icons/lucide.html")
