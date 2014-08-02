from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Desktop
from base.forms import NewDesktopForm
from django.contrib.auth.decorators import login_required




@login_required
def client_home(request):
    # get all users desktops
    my_desktops = Desktop.objects.all()

    form = NewDesktopForm()

    context = {
	'app_name' : 'vdc',
        'my_desktops': my_desktops,
        'form' : form,
    }
    return render(request, 'base/client_home.html', context)

@login_required
def create_desktop(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewDesktopForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    desktop = form.save(commit=False)
    	    desktop.save()
        else:
            print 'bad form: ', str(form)
    return HttpResponseRedirect('/') # Redirect home after POST

@login_required
def delete_desktop(request, desktop_name):
    if request.method == 'GET':
        desktop = Desktop.objects.get(name=desktop_name)
	if desktop != None:
	    desktop.delete()
    return HttpResponseRedirect('/') # Redirect home after DELETE
