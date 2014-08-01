from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Desktop
from base.forms import NewDesktopForm


def client_main_display(request):
    # get all users desktops
    my_desktops = Desktop.all()

    form = NewDesktopForm()

    context = {
	'app_name' : 'vdc',
        'my_desktops': my_desktops,
        'form' : form,
    }
    return render(request, 'base/clientMainDisplay.html', context)

_cloudfront_prefix = 'https://d2d9cpp21l4wuy.cloudfront.net/'
def mysql_add_student(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MySqlStudentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    student = form.save(commit=False)
            photo = request.FILES['student_photo']

	    key_name = s3.upload(photo)
	    photo_url = _cloudfront_prefix + key_name
            student.photo_url = photo_url

    	    student.save()
    return HttpResponseRedirect('/mysql') # Redirect home after POST

def mysql_delete_student(request, student_id):
    if request.method == 'GET':
        student = Student.objects.get(student_id=student_id)
	if student != None:
	    s3.delete_file(student.photo_url)
	    student.delete()
    return HttpResponseRedirect('/mysql') # Redirect home after DELETE





db_conn_details = {
    'table' : 'idc-cloud-ex2-dynamo-table',
    # credentials : in_boto_config,
}
cache_conn_details = { # TODO - move this to some config/properties file
    'host' : 'idc-cloud-ex2-cache.brlx8k.0001.use1.cache.amazonaws.com',
    'port' : 6379,
    'db'   : 0,
}

cache_db = cache_db.get_connection(db_conn_details, cache_conn_details)

def dynamo(request):
    # read latest 10 students
    latest_students = cache_db.get_latest(10)
    
    # make them presentable and serve them to the client
    #latest_students = map(cache_to_model, latest_students)
    form = DynamoStudentForm()
    context = {
        'app_name' : 'dynamo',
        'latest_students_list': latest_students,
        'form' : form,
    }
    return render(request, 'base/dynamo.html', context)

def dynamo_by_attribute(request, attribute):
    value = request.GET.get('q', '')
    # read latest 10 students
    students = cache_db.get_by_attribute(attribute, value)
    
    # make them presentable and serve them to the client
    #latest_students = map(cache_to_model, latest_students)
    form = DynamoStudentForm()
    context = {
        'app_name' : 'dynamo',
        'latest_students_list': students,
        'form' : form,
    }
    return render(request, 'base/dynamo.html', context)
    

def dynamo_add_student(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DynamoStudentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            photo = request.FILES['student_photo']

	    key_name = s3.upload(photo)
	    photo_url = _cloudfront_prefix + key_name


	    student = form.to_student()
	    student.photo_url = photo_url
    	    if  not cache_db.insert(student):
                raise Exception('failed inserting %s into cache_db', str(student))
    return HttpResponseRedirect('/dynamo')

def dynamo_delete_student(request, student_id):
    if request.method == 'GET':# TODO - change this to DELETE
        student = cache_db.get_by_id(student_id)
	if student != None:
	    #s3.delete_file(student.photo_url)
	    cache_db.remove(student_id)
    return HttpResponseRedirect('/dynamo')

def clear_dynamo(request):
    if request.method == 'GET':
        cache_db._clear()
        # TODO - clear images from s3
    return HttpResponseRedirect('/dynamo')
