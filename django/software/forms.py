from django import forms
from .models import Software



class SoftwareForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Software
        fields = '__all__'
        exclude = ('owner',)