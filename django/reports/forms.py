from django.utils.translation import gettext as _
from django import forms
from .models import Report, InputFiles, DumpFiles
from environments.models import Environment
from software.models import Software
from .fields import EnvironmentsChoiceField

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['environments'] = forms.ModelMultipleChoiceField(queryset=Environment.objects.all(), label = "Среды выполнения")
        self.fields['software'] = forms.ModelChoiceField(queryset=Software.objects.all(), widget=forms.NumberInput, label = "ПО")
        # self.fields['software'].widget.choices = []
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class InputFilesForm(forms.ModelForm):
    class Meta:
        model = InputFiles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InputFilesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DumpFilesForm(forms.ModelForm):
    class Meta:
        model = DumpFiles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DumpFilesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

InputFilesFormSet = forms.inlineformset_factory(Report, InputFiles, form=InputFilesForm, extra=1, can_delete=True, can_delete_extra=True)
DumpFilesFormSet = forms.inlineformset_factory(Report, DumpFiles, form=DumpFilesForm, extra=1, can_delete=True, can_delete_extra=True)

class SearchForm(forms.Form):
    title               = forms.CharField(strip=True, required=False, label="Название")
    cwe                 = forms.IntegerField(required=False, label="Номер CWE")
    software            = forms.IntegerField(required=False, label="ПО")
    exploitability_from = forms.IntegerField(initial=1, min_value=0, max_value=10, required=False, label="Экслуатабельность (от)")
    exploitability_to   = forms.IntegerField(initial=10, min_value=0, max_value=10, required=False, label="Экслуатабельность (до)")
    danger_from         = forms.IntegerField(initial=1, min_value=0, max_value=10, required=False, label="Опасность (от)")
    danger_to           = forms.IntegerField(initial=10, min_value=0, max_value=10, required=False, label="Опасность (до)")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        exploitability_from = cleaned_data.get("exploitability_from")
        exploitability_to = cleaned_data.get("exploitability_to")

        danger_from = cleaned_data.get("danger_from")
        danger_to = cleaned_data.get("danger_to")

        if (exploitability_from > exploitability_to):
            raise forms.ValidationError(_("Эксплуатабельность (до) не может быть больше эксплуатабельности (после)!"))
        
        if (danger_from > danger_to):
            raise forms.ValidationError(_("Опасность (до) не может быть больше опасность (после)!"))

        return cleaned_data