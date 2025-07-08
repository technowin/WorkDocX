from django.views.generic import TemplateView


# Create your views here.

class ExtendedView(TemplateView):
    pass

extended_dragula_view = ExtendedView.as_view(template_name="bootstrap/extended/dragula.html")
extended_range_slider_view = ExtendedView.as_view(template_name="bootstrap/extended/range-slider.html")
extended_ratings_view = ExtendedView.as_view(template_name="bootstrap/extended/ratings.html")
extended_scrollbar_view = ExtendedView.as_view(template_name="bootstrap/extended/scrollbar.html")
extended_scrollspy_view = ExtendedView.as_view(template_name="bootstrap/extended/scrollspy.html")
extended_treeview_view = ExtendedView.as_view(template_name="bootstrap/extended/treeview.html")