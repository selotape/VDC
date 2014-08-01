# import forms
from django import forms
from base.models import Desktop

# Create the form class.
class NewDesktopForm(forms.ModelForm):
    class Meta:
        model = Desktop
        fields = ['name', 'owner', 'ami', 'state', 'dns']
