from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

# Create your views here.

class PagesView(TemplateView):
    pass

pages_profile_view = PagesView.as_view(template_name="bootstrap/pages/profile.html")
pages_profile_2_view = PagesView.as_view(template_name="bootstrap/pages/profile-2.html")
pages_invoice_view = PagesView.as_view(template_name="bootstrap/pages/invoice.html")
pages_faq_view = PagesView.as_view(template_name="bootstrap/pages/faq.html")
pages_pricing_view = PagesView.as_view(template_name="bootstrap/pages/pricing.html")
pages_maintenance_view = PagesView.as_view(template_name="bootstrap/pages/maintenance.html")
pages_login_view = PagesView.as_view(template_name="bootstrap/pages/login.html")
pages_login_2_view = PagesView.as_view(template_name="bootstrap/pages/login-2.html")
pages_register_view = PagesView.as_view(template_name="bootstrap/pages/register.html")
pages_register_2_view = PagesView.as_view(template_name="bootstrap/pages/register-2.html")
pages_logout_view = PagesView.as_view(template_name="bootstrap/pages/logout.html")
pages_logout_2_view = PagesView.as_view(template_name="bootstrap/pages/logout-2.html")
pages_recoverpw_view = PagesView.as_view(template_name="bootstrap/pages/recoverpw.html")
pages_recoverpw_2_view = PagesView.as_view(template_name="bootstrap/pages/recoverpw-2.html")
pages_lock_screen_view = PagesView.as_view(template_name="bootstrap/pages/lock-screen.html")
pages_lock_screen_2_view = PagesView.as_view(template_name="bootstrap/pages/lock-screen-2.html")
pages_confirm_mail_view = PagesView.as_view(template_name="bootstrap/pages/confirm-mail.html")
pages_confirm_mail_2_view = PagesView.as_view(template_name="bootstrap/pages/confirm-mail-2.html")
pages_404_view = PagesView.as_view(template_name="bootstrap/pages/error-404.html")
pages_404_alt_view = PagesView.as_view(template_name="bootstrap/pages/error-404-alt.html")
pages_500_view = PagesView.as_view(template_name="bootstrap/pages/error-500.html")
pages_starter_view = PagesView.as_view(template_name="bootstrap/pages/starter.html")
pages_preloader_view = PagesView.as_view(template_name="bootstrap/pages/preloader.html")
pages_timeline_view = PagesView.as_view(template_name="bootstrap/pages/timeline.html")
