from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import Report, InputFiles, DumpFiles
from .forms import ReportForm, InputFilesFormSet, DumpFilesFormSet, SearchForm
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ReportsMenu(TemplateView):
    template_name = "reports/menu/menu.html"

class ReportCreate(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/new/new.html'

    def get_context_data(self, **kwargs):
        data = super(ReportCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inputfiles'] = InputFilesFormSet(self.request.POST, self.request.FILES)
            data['dumpfiles'] = DumpFilesFormSet(self.request.POST, self.request.FILES)

        if 'inputfiles' not in data:
            data['inputfiles'] = InputFilesFormSet()
        if 'dumpfiles' not in data:
            data['dumpfiles'] = DumpFilesFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()

        inputfiles = context['inputfiles']
        dumpfiles = context['dumpfiles']
        
        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()

            if inputfiles.is_valid():
                inputfiles.instance = self.object
                inputfiles.save()
            else:
                self.object.delete()
                return super().form_invalid(form=form)
            
            if dumpfiles.is_valid():
                dumpfiles.instance = self.object
                dumpfiles.save()
            else:
                self.object.delete()
                return super().form_invalid(form=form)
        
        return super(ReportCreate, self).form_valid(form)

class ReportList(ListView):
    model = Report
    paginate_by = 5
    template_name = 'reports/all/all.html'

    class Meta:
        ordering = ['-updated']

class ReportDetail(DetailView):
    model = Report
    context_object_name = 'report'
    template_name = 'reports/report/report.html'
    pk_url_kwarg = 'report_id'

class ReportUpdate(UserPassesTestMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update/update.html'
    pk_url_kwarg = 'report_id'   

    def get_context_data(self, **kwargs):
        data = super(ReportUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inputfiles'] = InputFilesFormSet(self.request.POST, self.request.FILES, instance=self.object)
            data['dumpfiles'] = DumpFilesFormSet(self.request.POST, self.request.FILES, instance=self.object)

        if 'inputfiles' not in data:
            data['inputfiles'] = InputFilesFormSet(instance=self.object)
        if 'dumpfiles' not in data:
            data['dumpfiles'] = DumpFilesFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()

        inputfiles = context['inputfiles']
        dumpfiles = context['dumpfiles']
        
        with transaction.atomic():
            self.object = form.save()

            if inputfiles.is_valid():
                inputfiles.instance = self.object
                inputfiles.save()
            else:
                self.object.delete()
                return super().form_invalid(form=form)
            
            if dumpfiles.is_valid():
                dumpfiles.instance = self.object
                dumpfiles.save()
            else:
                self.object.delete()
                return super().form_invalid(form=form)
        
        return super(ReportUpdate, self).form_valid(form)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False

class ReportDelete(UserPassesTestMixin, DeleteView):
    model = Report
    pk_url_kwarg = 'report_id'
    success_url = reverse_lazy('all_reports')
    template_name = 'reports/delete/delete.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False

class SearchView(FormView):
    template_name = "reports/search/search.html"
    form_class = SearchForm
    success_url = reverse_lazy('search')

class SearchResultsList(ListView):
    model = Report
    paginate_by = 5
    template_name = 'reports/search/results/results.html'

    def get_queryset(self):
        object_list = Report.objects.all()
        query_dict = self.request.GET

        # By Title
        if query_dict.get('title', None):
            object_list = object_list.filter(title__icontains=query_dict['title'])

        # By CWE
        if query_dict.get('cwe', None):
            object_list = object_list.filter(cwe__exact=query_dict['cwe'])

        # By Software
        if query_dict.get('software', None):
            object_list = object_list.filter(software__exact=query_dict['software'])

        # By Exploitability
        if query_dict.get('exploitability_from', None):
            object_list = object_list.filter(exploitability__gte=query_dict['exploitability_from'])
        if query_dict.get('exploitability_to', None):
            object_list = object_list.filter(exploitability__lte=query_dict['exploitability_to'])

        # By Danger
        if query_dict.get('danger_from', None):
            object_list = object_list.filter(danger__gte=query_dict['danger_from'])
        if query_dict.get('danger_to', None):
            object_list = object_list.filter(danger__lte=query_dict['danger_to'])

        return object_list

    def get(self, request, *args, **kwargs):
        param_dict = request.GET.dict()

        if (not param_dict):
            messages.error(self.request, 'Не указаны параметры')
            self.object_list = Report.objects.none()
            ctx = self.get_context_data(**kwargs)
            ctx['params'] = False
            return render(self.request, self.template_name, ctx)
        else:
            return super().get(self, request, *args, **kwargs)
        
    class Meta:
        ordering = ['-updated']

