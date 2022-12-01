from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import ProfileUpdateForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "registration/profile_form.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
