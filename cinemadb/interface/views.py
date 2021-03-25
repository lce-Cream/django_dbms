from django.shortcuts import redirect, render
# from .forms import StudentForm
# from .models import Student

def home(request):
    # student_list = Student.objects.all()
    content = {'tab_title': 'home'}
    return render(request, 'interface/home.html', content)