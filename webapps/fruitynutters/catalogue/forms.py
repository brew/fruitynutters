from django import forms
from django.apps import apps
from widgets import WYMEditor


class PageAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=WYMEditor())

    class Meta:
        model = apps.get_model('catalogue', 'Page')
        fields = "__all__"
