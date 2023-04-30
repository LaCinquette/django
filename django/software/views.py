from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Software
from .forms import SoftwareForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect


class NewSoftware(CreateView):
    model = Software
    form_class = SoftwareForm
    template_name = 'software/new/new.html'
    # success_url = reverse_lazy('all_software')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()        
        # return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)
    
class SoftwareUpdate(UserPassesTestMixin, UpdateView):
    model = Software
    form_class = SoftwareForm
    pk_url_kwarg = 'software_id'
    template_name = 'software/update/update.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False

class SoftwareDelete(UserPassesTestMixin, DeleteView):
    model = Software
    pk_url_kwarg = 'software_id'
    success_url = reverse_lazy('all_software')
    template_name = 'software/delete/delete.html' 

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False 

class DetailSoftware(DetailView):
    model = Software
    context_object_name = 'software'
    template_name = 'software/software/software.html'
    pk_url_kwarg = 'software_id'

class ListSoftware(ListView):
    model = Software
    paginate_by = 5
    template_name = 'software/all/all.html'