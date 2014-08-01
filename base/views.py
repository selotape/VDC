from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Desktop
from base.forms import NewDesktopForm


def client_home(request):
    # get all users desktops
    my_desktops = Desktop.all()

    form = NewDesktopForm()

    context = {
	'app_name' : 'vdc',
        'my_desktops': my_desktops,
        'form' : form,
    }
    return render(request, 'base/clientMainDisplay.html', context)

def create_desktop(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewDesktopFrom(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    desktop = form.save(commit=False)
    	    desktop.save()
    return HttpResponseRedirect('/') # Redirect home after POST

def delete_desktop(request, desktop_name):
    if request.method == 'GET':
        desktop = Student.objects.get(name=desktop_name)
	if desktop != None:
	    desktop.delete()
    return HttpResponseRedirect('/') # Redirect home after DELETE
