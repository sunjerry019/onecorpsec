from django import forms

from .models import getTable

class companyEditForm(forms.ModelForm):
    def __init__(self, _model):
        # super(companyEditForm, self).__init__()
        self.Meta = companyEditForm.Meta(_model)

    class Meta:
        def __init__(self, _mdl):
            self.model = _mdl
            self.fields = ('toemail', 'ccemail', 'bccemail', 'addressename')
