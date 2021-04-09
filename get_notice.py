from django.contrib.auth.decorators import login_required
from batches.models import Notice
from students.models import AddStudentInst
from accounts.models import Teacher,Student,Institute
from django.contrib.auth.models import User
from teacher.models import enrollTutors

@login_required(login_url="Login")
def notice(request):
    if request.session['type'] == 'Student':
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        batches_obj = AddStudentInst.objects.filter(student=student) 
        batch_set = set()
        for i in batches_obj:
            batch_set.add(i.batch)
        notice = Notice.objects.filter(batch__batchName__in=list(batch_set)).order_by('-id')
        return notice
    elif request.session['type'] == 'Teacher':
        user = User.objects.get(username=request.session['user'])
        teacher = Teacher.objects.get(user=user)
        teacher_enroll = enrollTutors.objects.filter(teacher=teacher)
        teacher_courses = set()
        for i in teacher_enroll:
            teacher_courses.add(i.courseName)
        notice = Notice.objects.filter(batch__course__courseName__in=list(teacher_courses)).order_by('-id')
        return notice
    elif request.session['type'] == 'Institute':
        user = User.objects.get(username=request.session['user'])
        institute = Institute.objects.get(user=user)
        notice = Notice.objects.filter(batch__institute=institute)
        return notice
    else:
        return None