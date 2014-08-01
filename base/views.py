""" Views for the base application """
from django.shortcuts import render
# from base.models import Student

# Create your views here.
def home(request):
    latest_students_list = Student.objects.all().order_by('-creation_date')[:10]
    context = {'latest_students_list': latest_students_list}
    return render(request, 'base/home.html', context)
