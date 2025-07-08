from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

# Create your views here.


class ChartsView(TemplateView):
    pass



charts_apex_area_view = ChartsView.as_view(template_name="bootstrap/charts/apex/area.html")
charts_apex_bar_view = ChartsView.as_view(template_name="bootstrap/charts/apex/bar.html")
charts_apex_bubble_view = ChartsView.as_view(template_name="bootstrap/charts/apex/bubble.html")
charts_apex_candlestick_view = ChartsView.as_view(template_name="bootstrap/charts/apex/candlestick.html")
charts_apex_column_view = ChartsView.as_view(template_name="bootstrap/charts/apex/column.html")
charts_apex_heatmap_view = ChartsView.as_view(template_name="bootstrap/charts/apex/heatmap.html")
charts_apex_line_view = ChartsView.as_view(template_name="bootstrap/charts/apex/line.html")
charts_apex_mixed_view = ChartsView.as_view(template_name="bootstrap/charts/apex/mixed.html")
charts_apex_timline_view = ChartsView.as_view(template_name="bootstrap/charts/apex/timeline.html")
charts_apex_boxplot_view = ChartsView.as_view(template_name="bootstrap/charts/apex/boxplot.html")
charts_apex_treemap_view = ChartsView.as_view(template_name="bootstrap/charts/apex/treemap.html")
charts_apex_pie_view = ChartsView.as_view(template_name="bootstrap/charts/apex/pie.html")
charts_apex_radar_view = ChartsView.as_view(template_name="bootstrap/charts/apex/radar.html")
charts_apex_radialbar_view = ChartsView.as_view(template_name="bootstrap/charts/apex/radialbar.html")
charts_apex_scatter_view = ChartsView.as_view(template_name="bootstrap/charts/apex/scatter.html")
charts_apex_polararea_view =ChartsView.as_view(template_name="bootstrap/charts/apex/polar-area.html")
charts_apex_sparklines_view = ChartsView.as_view(template_name="bootstrap/charts/apex/sparklines.html")
charts_chartjs_area_view = ChartsView.as_view(template_name="bootstrap/charts/chartjs/area.html")
charts_chartjs_bar_view = ChartsView.as_view(template_name="bootstrap/charts/chartjs/bar.html")
charts_chartjs_line_view = ChartsView.as_view(template_name="bootstrap/charts/chartjs/line.html")
charts_chartjs_other_view = ChartsView.as_view(template_name="bootstrap/charts/chartjs/other.html")
charts_brite_view = ChartsView.as_view(template_name="bootstrap/charts/brite.html")
charts_sparkline_view = ChartsView.as_view(template_name="bootstrap/charts/sparklines.html")
