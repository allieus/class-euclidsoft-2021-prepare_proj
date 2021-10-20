from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from accounts.forms import SignupForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/form.html"


class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/form.html"
    success_url = reverse_lazy("accounts:login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
