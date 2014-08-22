# import forms
from django import forms
from base.models import Desktop

class NewDesktopForm(forms.Form):
    AMI_CHOICES = (
        ('ami-864d84ee', 'Trusty Tahr'),
        ('ami-9ade1df2', 'Windows 2012R2'),
    )
 
    name = forms.CharField(max_length=100)
    ami = forms.ChoiceField(choices=AMI_CHOICES)
