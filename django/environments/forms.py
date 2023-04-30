from django import forms
from .models import Environment



class EnvironmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Environment
        fields = '__all__'
        exclude = ('owner',)