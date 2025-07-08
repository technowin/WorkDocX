from django.views.generic import TemplateView

# Create your views here.

class UiView(TemplateView):
    pass


ui_accordions_view = UiView.as_view(template_name="bootstrap/ui/accordions.html")
ui_alerts_view = UiView.as_view(template_name="bootstrap/ui/alerts.html")
ui_avatars_view = UiView.as_view(template_name="bootstrap/ui/avatars.html")
ui_badges_view = UiView.as_view(template_name="bootstrap/ui/badges.html")
ui_breadcrumb_view = UiView.as_view(template_name="bootstrap/ui/breadcrumb.html")
ui_buttons_view = UiView.as_view(template_name="bootstrap/ui/buttons.html")
ui_cards_view = UiView.as_view(template_name="bootstrap/ui/cards.html")
ui_carousel_view = UiView.as_view(template_name="bootstrap/ui/carousel.html")
ui_dropdowns_view = UiView.as_view(template_name="bootstrap/ui/dropdowns.html")
ui_embed_video_view = UiView.as_view(template_name="bootstrap/ui/embed-video.html")
ui_grid_view = UiView.as_view(template_name="bootstrap/ui/grid.html")
ui_list_group_view = UiView.as_view(template_name="bootstrap/ui/list-group.html")
ui_modals_view = UiView.as_view(template_name="bootstrap/ui/modals.html")
ui_notifications_view = UiView.as_view(template_name="bootstrap/ui/notifications.html")
ui_offcanvas_view = UiView.as_view(template_name="bootstrap/ui/offcanvas.html")
ui_placeholders_view = UiView.as_view(template_name="bootstrap/ui/placeholders.html")
ui_pagination_view = UiView.as_view(template_name="bootstrap/ui/pagination.html")
ui_popovers_view = UiView.as_view(template_name="bootstrap/ui/popovers.html")
ui_progress_view = UiView.as_view(template_name="bootstrap/ui/progress.html")
ui_ribbons_view = UiView.as_view(template_name="bootstrap/ui/ribbons.html")
ui_spinners_view = UiView.as_view(template_name="bootstrap/ui/spinners.html")
ui_tabs_view = UiView.as_view(template_name="bootstrap/ui/tabs.html") 
ui_tooltips_view = UiView.as_view(template_name="bootstrap/ui/tooltips.html")
ui_links_view = UiView.as_view(template_name="bootstrap/ui/links.html")
ui_typography_view = UiView.as_view(template_name="bootstrap/ui/typography.html")
ui_utilities_view = UiView.as_view(template_name="bootstrap/ui/utilities.html")
