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
        self.fields['environments'] = forms.ModelMultipleChoiceField(queryset=Environment.objects.all())
        self.fields['software'] = forms.ModelChoiceField(queryset=Software.objects.all(), widget=forms.NumberInput)
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
    title               = forms.CharField(strip=True, required=False)
    cwe                 = forms.IntegerField(required=False)
    software            = forms.IntegerField(required=False)
    exploitability_from = forms.IntegerField(label="Exploitability from", initial=1, min_value=0, max_value=10, required=False)
    exploitability_to   = forms.IntegerField(label="Exploitability to", initial=10, min_value=0, max_value=10, required=False)
    danger_from         = forms.IntegerField(label="Danger from", initial=1, min_value=0, max_value=10, required=False)
    danger_to           = forms.IntegerField(label="Danger to", initial=10, min_value=0, max_value=10, required=False)

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
            raise forms.ValidationError(_("Exploitability to can't be lower than exploitability from!"))
        
        if (danger_from > danger_to):
            raise forms.ValidationError(_("Danger to can't be lower than danger from!"))

        return cleaned_data