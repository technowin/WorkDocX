from django.urls import path

from .views import (

    pages_profile_view,
    pages_profile_2_view,
    pages_invoice_view,
    pages_faq_view,
    pages_pricing_view,
    pages_maintenance_view,
    pages_login_view,
    pages_login_2_view,
    pages_register_view,
    pages_register_2_view,
    pages_logout_view,
    pages_logout_2_view,
    pages_recoverpw_view,
    pages_recoverpw_2_view,
    pages_lock_screen_view,
    pages_lock_screen_2_view,
    pages_confirm_mail_view,
    pages_confirm_mail_2_view,
    pages_404_view,
    pages_404_alt_view,
    pages_500_view,
    pages_starter_view,
    pages_preloader_view,
    pages_timeline_view
)


app_name = "pages"
urlpatterns = [

    path("profile", view=pages_profile_view, name="profile"),
    path("profile-2", view=pages_profile_2_view, name="profile-2"),
    path("invoice", view=pages_invoice_view, name="invoice"),
    path("faq", view=pages_faq_view, name="faq"),
    path("pricing", view=pages_pricing_view, name="pricing"),
    path("maintenance", view=pages_maintenance_view, name="maintenance"),
    path("login", view=pages_login_view, name="login"),
    path("login-2", view=pages_login_2_view, name="login-2"),
    path("register", view=pages_register_view, name="register"),
    path("register-2", view=pages_register_2_view, name="register-2"),
    path("logout", view=pages_logout_view, name="logout"),
    path("logout-2", view=pages_logout_2_view, name="logout-2"),
    path("recoverpw", view=pages_recoverpw_view, name="recoverpw"),
    path("recoverpw-2", view=pages_recoverpw_2_view, name="recoverpw-2"),
    path("lock-screen", view=pages_lock_screen_view, name="lock-screen"),
    path("lock-screen-2", view=pages_lock_screen_2_view, name="lock-screen-2"),
    path("confirm-mail", view=pages_confirm_mail_view, name="confirm-mail"),
    path("confirm-mail-2", view=pages_confirm_mail_2_view, name="confirm-mail-2"),
    path("404", view=pages_404_view, name="404"),
    path("404-alt", view=pages_404_alt_view, name="404-alt"),
    path("500", view=pages_500_view, name="500"),
    path("starter", view=pages_starter_view, name="starter"),
    path("preloader", view=pages_preloader_view, name="preloader"),
    path("timeline", view=pages_timeline_view, name="timeline")
]
