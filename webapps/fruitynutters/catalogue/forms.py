from django import forms
from django.db.models import get_model
from widgets import WYMEditor


class PageAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=WYMEditor())

    class Meta:
        model = get_model('catalogue', 'Page')
