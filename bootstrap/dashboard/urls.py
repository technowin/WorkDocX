from django.urls import path

from .views import (index_dashboard_view, analytics_dashboard_view,
                    projects_dashboard_view, wallet_dashboard_view, crm_dashboard_view, widgets_view,

                    # demo
                    demo_saas_index_dark_view,
                    demo_saas_index_rtl_view,
                    demo_creative_horizontal_view,
                    demo_creative_horizontal_dark_view,
                    demo_creative_horizontal_rtl_view,
                    demo_modern_detached_view,
                    demo_modern_detached_dark_view,
                    demo_modern_detached_rtl_view,
                    demo_index_light_sidenav_layout,
                    demo_horizontal_boxed_layout,
                    demo_full_light_layout,
                    demo_full_dark_layout,
                    demo_full_rtl_layout
                    )

app_name = "dashboard"
urlpatterns = [
    path("index", view=index_dashboard_view, name="index"),
    path("analytics", view=analytics_dashboard_view, name="analytics"),
    path("projects", view=projects_dashboard_view, name="projects"),
    path("crm", view=crm_dashboard_view, name="crm"),
    path("wallet", view=wallet_dashboard_view, name="wallet"),
    path("widgets", view=widgets_view, name="widgets"),

    # demo
    path("demo-saas-dark", view=demo_saas_index_dark_view, name="demo.saas-dark"),
    path("demo-saas-rtl", view=demo_saas_index_rtl_view, name="demo.saas-rtl"),
    path("demo-horizontal-creative", view=demo_creative_horizontal_view, name="demo.horizontal-creative"),
    path("demo-horizontal-creative-dark", view=demo_creative_horizontal_dark_view,
         name="demo.horizontal-creative-dark"),
    path("demo-horizontal-creative-rtl", view=demo_creative_horizontal_rtl_view, name="demo.horizontal-creative-rtl"),
    path("demo-detached-modern", view=demo_modern_detached_view, name="demo.detached-modern"),
    path("demo-detached-modern-dark", view=demo_modern_detached_dark_view, name="demo.detached-modern-dark"),
    path("demo-detached-modern-rtl", view=demo_modern_detached_rtl_view, name="demo.detached-modern-rtl"),

    path("demo-index-light-sidenav-layout", view=demo_index_light_sidenav_layout,
         name="demo.index-light-sidenav-layout"),
    path("demo-horizontal-boxed", view=demo_horizontal_boxed_layout, name="demo.horizontal-boxed"),

    path("demo-full-light", view=demo_full_light_layout, name="demo.full-light"),
    path("demo-full-dark", view=demo_full_dark_layout, name="demo.full-dark"),
    path("demo-full-rtl", view=demo_full_rtl_layout, name="demo.full-rtl")
]
