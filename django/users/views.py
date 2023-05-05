from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from users.forms import LoginUserForm
from django.contrib.auth.models import User

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super(LoginUser, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
    
def logout_user(request):
    logout(request)
    return redirect('login')

def view_404(request, exception):
    print('Logged in:', request.user.is_authenticated)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) # redirect('login')
    return HttpResponseRedirect(reverse('profile')) # redirect('profile')
