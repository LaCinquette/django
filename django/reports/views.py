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
        
        # if (not inputfiles.is_valid()) or (not dumpfiles.is_valid()):
        #     return self.render_to_response(self.get_context_data(form=form))
        
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

        

        # user = self.request.user
        # form.instance.added_by = user
        # context = self.get_context_data()
        # leadqualificationsforms = context['leadqualifications']
        # leademploymentsforms    = context['leademployments']
        # leadreferencesforms     = context['leadreferences']
        # leadkinsforms           = context['leadkins']
        # with transaction.atomic():
        #     form.instance.Lead = self.request.user
        #     self.object = form.save()
        #     if leadqualificationsforms.is_valid():
        #         leadqualificationsforms.instance = self.object
        #         leadqualificationsforms.save()
        #     else:
        #         print('qulification form is invalid')
        #         self.object.delete()
        #         return super(LeadCreate, self).form_invalid(form)  
            
        #     if leademploymentsforms.is_valid():
        #             leademploymentsforms.instance = self.object
        #             leademploymentsforms.save()
        #     else:
        #         print('employment form is invalid')
        #         self.object.delete()
        #         return super(LeadCreate, self).form_invalid(form)  

        #     if leadreferencesforms.is_valid():
        #         leadreferencesforms.instance = self.object
        #         leadreferencesforms.save()
        #     else:
        #         print('referencesforms form is invalid')
        #         self.object.delete()
        #         return super(LeadCreate, self).form_invalid(form)  
        #     if leadkinsforms.is_valid():
        #         leadkinsforms.instance = self.object
        #         leadkinsforms.save()
        #     else:
        #         print('Kin form is invalid')
        #         self.object.delete()
        #         return super(LeadCreate, self).form_invalid(form)
        # usergroup=self.request.user.get_user_group()
        # if usergroup.name == "agent":
        #     print('usergroup agent',usergroup)
        #     form.instance.Agent=self.request.user
        #     form.instance.Status=Student_status[-1][0]
        # elif usergroup.name == "staff":
        #     form.instance.Responsible=self.request.user
        # form.save()


        # try:
        #     with transaction.atomic():
        #         print("input", inputfiles.is_valid())
        #         print("dump", dumpfiles.is_valid())
        #         if inputfiles.is_valid() and dumpfiles.is_valid():
        #             print("all valid")

        #             self.object = form.save()

        #             inputfiles.instance = self.object
        #             inputfiles.save()

        #             dumpfiles.instance = self.object
        #             dumpfiles.save()
        #         else:
        #             raise IntegrityError
            
        # except IntegrityError:
        #     print("Integrity Error") # заглушка

        
        return super(ReportCreate, self).form_valid(form)

class ReportList(ListView):
    model = Report
    paginate_by = 5
    template_name = 'reports/all/all.html'

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
            # form.instance.owner = self.request.user
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
    
    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user
    #     report = self.get_object()
    #     if not (report.owner == user or user.is_staff):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)
    
    # def get_object(self, *args, **kwargs):
    #     obj = super().get_object(*args, **kwargs)
    #     if obj.author != self.request.user:
    #         raise PermissionDenied()
    #     return obj
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.owner or self.request.user.is_staff:
            return True
        return False
    # def post

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
        # queryset = super().get_queryset()
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
        # request.pat
        if (not param_dict):
            # print(request.path)
            messages.error(self.request, 'Не указаны параметры')
            self.object_list = Report.objects.none()
            ctx = self.get_context_data(**kwargs)
            ctx['params'] = False
            return render(self.request, self.template_name, ctx)
        else:
            return super().get(self, request, *args, **kwargs)





# class ReportInline():

#     def form_valid(self, form):
#         named_formsets = self.get_named_formsets()
#         if not all((x.is_valid() for x in named_formsets.values())):
#             return self.render_to_response(self.get_context_data(form=form))

#         self.object = form.save()

#         # for every formset, attempt to find a specific formset save function
#         # otherwise, just save.
#         for name, formset in named_formsets.items():
#             formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
#             if formset_save_func is not None:
#                 formset_save_func(formset)
#             else:
#                 formset.save()
#         return redirect('all_reports')

#     def formset_inputfiles_valid(self, formset):
#         """
#         Hook for custom formset saving. Useful if you have multiple formsets
#         """
#         inputfiles = formset.save(commit=False)  # self.save_formset(formset, contact)
#         # add this 2 lines, if you have can_delete=True parameter 
#         # set in inlineformset_factory func
#         for obj in formset.deleted_objects:
#             obj.delete()
#         for inputfile in inputfiles:
#             inputfile.report = self.object
#             inputfile.save()

#     def formset_dumpfiles_valid(self, formset):
#         """
#         Hook for custom formset saving. Useful if you have multiple formsets
#         """
#         dumpfiles = formset.save(commit=False)  # self.save_formset(formset, contact)
#         # add this 2 lines, if you have can_delete=True parameter 
#         # set in inlineformset_factory func
#         for obj in formset.deleted_objects:
#             obj.delete()
#         for dumpfile in dumpfiles:
#             dumpfile.report = self.object
#             dumpfile.save()

# class ReportCreate(ReportInline, CreateView):
#     form_class = ReportForm
#     model = Report
#     template_name = "reports/new/new2.html"

#     def get_context_data(self, **kwargs):
#         ctx = super(ReportCreate, self).get_context_data(**kwargs)
#         ctx['named_formsets'] = self.get_named_formsets()
#         return ctx

#     def get_named_formsets(self):
#         if self.request.method == "GET":
#             return {
#                 'inputfiles': InputFilesFormSet(prefix='inputfiles'),
#                 'dumpfiles': DumpFilesFormSet(prefix='dumpfiles'),
#             }
#         else:
#             return {
#                 'inputfiles': InputFilesFormSet(self.request.POST or None, self.request.FILES or None, prefix='inputfiles'),
#                 'dumpfiles': DumpFilesFormSet(self.request.POST or None, self.request.FILES or None, prefix='dumpfiles'),
#             }


# # class ReportUpdate(ReportInline, UpdateView):

# #     def get_context_data(self, **kwargs):
# #         ctx = super(ReportUpdate, self).get_context_data(**kwargs)
# #         ctx['named_formsets'] = self.get_named_formsets()
# #         return ctx

# #     def get_named_formsets(self):
# #         return {
# #             'inputfiles': InputFilesFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='inputfiles'),
# #             'dumpfiles': DumpFilesFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='dumpfiles'),
# #         }

# def delete_inputfile(request, pk):
#     try:
#         inputfile = InputFiles.objects.get(id=pk)
#     except InputFiles.DoesNotExist:
#         messages.success(
#             request, 'Object Does not exit'
#             )
#         return redirect('update_report', pk=inputfile.report.id)

#     inputfile.delete()
#     messages.success(
#             request, 'Image deleted successfully'
#             )
#     return redirect('update_report', pk=inputfile.report.id)


# def delete_dumpfile(request, pk):
#     try:
#         dumpfile = DumpFiles.objects.get(id=pk)
#     except dumpfile.DoesNotExist:
#         messages.success(
#             request, 'Object Does not exit'
#             )
#         return redirect('update_report', pk=dumpfile.report.id)

#     dumpfile.delete()
#     messages.success(
#             request, 'Variant deleted successfully'
#             )
#     return redirect('update_report', pk=dumpfile.report.id)
