from django.views.generic import TemplateView

# Create your views here.

class TablesView(TemplateView):
    pass

tables_basic_view = TablesView.as_view(template_name="bootstrap/tables/basic.html")
tables_datatable_view = TablesView.as_view(template_name="bootstrap/tables/datatable.html")
    