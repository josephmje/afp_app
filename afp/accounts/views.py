from django.views.generic import UpdateView
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import ProfileUpdateForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "registration/profile_form.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
