from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
)    # cambiar
from django.contrib.auth import get_user_model
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
)    # cambiar
from django.urls import reverse    # Apéndice
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView
)    # Apéndice
from django.contrib.auth.mixins import UserPassesTestMixin    # Apéndice


User = get_user_model()
# Hasta aquí

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm   # cambiar
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tasks:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_pw)
        login(self.request, user)
        return response
class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, DetailView):    # cambiar
    model = User
    template_name = 'accounts/user_detail.html'
# Hasta aquí

class UserUpdate(OnlyYouMixin, UpdateView):    # cambiar
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})

class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/user_detail.html'

class UserDelete(OnlyYouMixin, DeleteView):    # cambiar
    model = User
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')
