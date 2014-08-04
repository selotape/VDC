from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Desktop
from base.forms import NewDesktopForm
from django.contrib.auth.decorators import login_required
#from vdc.VDCConnection import VDCConnection

# Put boto_config.ini in home directory
#conn = VDCConnection()

@login_required
def client_home(request):

    # get all users desktops
    # conn.get_all_machines(tags={"owner":request.user.username})
    my_desktops = Desktop.objects.filter(owner=request.user.username)

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
            #conn.create_machine(form.name, ami, is_windows, key_name, key_data, username, password, tags={"owner":request.user.username})
            desktop = form.save(commit=False)
            desktop.owner = request.user.username
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
