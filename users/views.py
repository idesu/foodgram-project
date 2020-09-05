from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # TODO: Вставить url страницы логина
    success_url = reverse_lazy("admin:auth_user_changelist")
    template_name = "reg.html"
