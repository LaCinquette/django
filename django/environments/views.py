from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import Environment
from .forms import EnvironmentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

class EnvironmentsMenu(TemplateView):
    template_name = "environments/menu/menu.html"

class NewEnvironment(CreateView):
    model = Environment
    form_class = EnvironmentForm
    template_name = 'environments/new/new.html'
    # success_url = reverse_lazy('all_environments')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()        
        return super().form_valid(form)
    
class EnvironmentUpdate(UserPassesTestMixin, UpdateView):
    model = Environment
    form_class = EnvironmentForm
    pk_url_kwarg = 'environment_id'
    template_name = 'environments/update/update.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False

class EnvironmentDelete(UserPassesTestMixin, DeleteView):
    model = Environment
    success_url = reverse_lazy('all_environments')
    pk_url_kwarg = 'environment_id'
    template_name = 'environments/delete/delete.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False

class DetailEnvironment(DetailView):
    model = Environment
    context_object_name = 'environment'
    template_name = 'environments/environment/environment.html'
    pk_url_kwarg = 'environment_id'

class ListEnvironments(ListView):
    model = Environment
    paginate_by = 5
    template_name = 'environments/all/all.html'