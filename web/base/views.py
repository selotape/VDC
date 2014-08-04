from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Desktop
from base.forms import NewDesktopForm
from django.contrib.auth.decorators import login_required
from VDCConnection import VDCConnection
from MachineDetails import MachineDetails
from utils import switch
import Consts

vdc = VDCConnection()

@login_required
def client_home(request):

    my_desktops = vdc.get_all_machines()# tags = {'owner':request.user.username, })
    
    form = NewDesktopForm()

    context = {
        'my_desktops': my_desktops,
        'form' : form,
    }
    return render(request, 'base/client_home.html', context)

@login_required
def create_desktop(request):
    if request.method == 'POST': 
        form = NewDesktopForm(request.POST) # A form bound to the POST data
        if form.is_valid():
             ami_field = form['ami']
             vdc.create_machine(form['name'], form['ami'].value(), 
                 key_name='idc-ex2-kp', tags={'owner':request.user.username, })
        else:
            print 'bad form: ', str(form)
    return HttpResponseRedirect('/') # Redirect home

@login_required
def delete_desktop(request, desktop_id):
    vdc.terminate_machine(desktop_id)
    return HttpResponseRedirect('/') # Redirect home


@login_required
def toggle_state(request, current_state, desktop_id):
    for case in switch(current_state):
        if case(Consts.RUNNING):
            vdc.stop_usage(desktop_id)
            print 'desktop was running. now shut down'
            break
        if case(Consts.STANDBY):
            vdc.start_usage(desktop_id)
            print 'desktop was shutdown. now running'
            break
        if case(): # default
            print "current_state \'"+current_state+"\' is unknown"
    return HttpResponseRedirect('/') # Redirect home
    
