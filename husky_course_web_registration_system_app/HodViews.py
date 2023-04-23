from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

from .forms import AddStudentForm, EditStudentForm, AddClassroomForm, EditClassroomForm, AddTeacherForm
from .models import Campuses, CustomUser, Department, InstructionalMethod, Staffs, Courses, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, Classrooms, Teacher


def admin_home(request):

    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    departments = Department.objects.all()
    department_course_num = {}
    department_student_num = {}
    department_registered_student_num = {}
    department_course_list = {}


    for department in departments:
        department_teachers = Teacher.objects.filter(department_id=department)
        department_course_count = 0
        department_courses = []
        for teacher in department_teachers:
            department_course_count += Courses.objects.filter(teacher_id=teacher).count()
            courses = Courses.objects.filter(teacher_id=teacher)
            for course in courses:
                department_courses.append(course)

        department_course_num[department]=department_course_count
        department_course_list[department]=department_courses
        department_registered_student_num[department]=Students.objects.filter(department_id=department, is_approved=True).count()
        department_student_num[department]=Students.objects.filter(department_id=department).count()
    
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # For Saffs
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []

    staffs = Staffs.objects.all()
    for staff in staffs:
        #print("---staff.admin:", staff.admin)
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id,
                                                 leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id,
                                                     status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id,
                                                 status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id,
                                                   leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
        "departments": departments,
        "department_registered_student_num": department_registered_student_num,
        "department_course_num": department_course_num,
        "department_student_num": department_student_num,
        "department_course_list": department_course_list
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, "hod_template/add_staff_template.html", context)


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)
        print("1")
        try:
            user = CustomUser()
            user.username = username
            user.email = email
            user.password = password
            user.user_type = 2
            user.first_name = first_name
            user.last_name = last_name
            user.last_logout = datetime.now()
            user.save()

            user.staffs.address = address
            user.staffs.department_id = department
            user.save()

            # Staffs.objects.create(admin=user)
            # advisor = Staffs.objects.get(admin=user)
            # advisor.address = address
            # advisor.department_id = department
            # advisor.save()


            # user = CustomUser.objects.create_user(username=username,
            #                                       password=password,
            #                                       email=email,
            #                                       first_name=first_name,
            #                                       last_name=last_name,
            #                                       user_type=2)

            # user.staffs.address = address
            # user.staffs.department_id = department
            # user.save()

            # staff_model = Staffs(username=username,
            # password=password,
            # email=email,
            # first_name=first_name,
            # last_name=last_name,
            # address=address,
            # department_id=department
            # )
            # print("11")
            # staff_model.save()

            messages.success(request, "Advisor Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Advisor!")
            return redirect('add_staff')


def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    departments = Department.objects.all()
    context = {
        "staff": staff,
        "id": staff_id,
        "departments": departments
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        department_id = request.POST.get('department_id')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            department = Department.objects.get(id=department_id)
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.department_id = department
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            import traceback
            traceback.print_exc()

            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)


def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


def add_course(request):
    campuses = Campuses.objects.all()
    teachers = Teacher.objects.all()

    classrooms = Classrooms.objects.filter(is_assigned='false')
    methods = InstructionalMethod.objects.all()
    departments = Department.objects.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    context = {
        "campuses": campuses,
        "teachers": teachers,
        'classrooms': classrooms,
        'departments': departments,
        'methods': methods,
        'days': days
    }
    return render(request, "hod_template/add_course_template.html", context)


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        campus_id = request.POST.get('campus')
        teacher_id = request.POST.get('teacher')
        classroom_id = request.POST.get('classroom')
        capacity = request.POST.get('capacity')
        day = request.POST.get('day')
        time = request.POST.get('time')
        method_id = request.POST.get('method')

        campus = Campuses.objects.get(id=campus_id)
        teacher = Teacher.objects.get(id=teacher_id)
        classroom = Classrooms.objects.get(id=classroom_id)
        method = InstructionalMethod.objects.get(id=method_id)
        if classroom.campus_id != campus:
            messages.error(request, "Course and Classroom should Belong to the Same Campus!")
            return redirect('add_course')
        try:
            course_model = Courses(course_name=course, campus_id=campus,
                                   teacher_id=teacher, classroom_id=classroom,
                                   capacity=capacity, instructional_method=method,
                                   day=day, time=time)
            course_model.save()
            classroom.is_assigned = 'true'
            classroom.save()
            messages.success(request, "Course Added Successfully!")
            return redirect('add_course')
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect('add_course')


def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses,
    }
    return render(request, 'hod_template/manage_course_template.html', context)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    teachers = Teacher.objects.all()
    classrooms = Classrooms.objects.filter(is_assigned='false')
    methods = InstructionalMethod.objects.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    context = {
        "course": course,
        "id": course_id,
        'teachers': teachers,
        'classrooms': classrooms,
        'methods': methods,
        'days': days,
    }
    return render(request, 'hod_template/edit_course_template.html', context)


def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')
        teacher_id = request.POST.get('teacher')
        campus_id = request.POST.get('campus')
        method_id = request.POST.get('method')
        classroom_id = request.POST.get('classroom')
        capacity = request.POST.get('capacity')
        day = request.POST.get('day')
        time = request.POST.get('time')

        teacher = Teacher.objects.get(id=teacher_id)
        campus = Campuses.objects.get(id=campus_id)
        method = InstructionalMethod.objects.get(id=method_id)
        classroom = Classrooms.objects.get(id=classroom_id)

        if classroom.campus_id != campus:
            messages.error(request, "Course and Classroom should Belong to the Same Campus!")
            return redirect('/edit_course/'+course_id)
        
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.teacher_id = teacher
            course.campus_id = campus
            course.instructional_method = method
            course.classroom_id = classroom
            course.capacity = capacity
            course.day = day
            course.time = time
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)


def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "hod_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year,
                                           session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            # session_year_id = form.cleaned_data['session_year_id']
            # course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            department_id = form.cleaned_data['department_id']
            department = Department.objects.get(id=department_id)

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser()
                user.username = username
                user.email = email
                user.password = password
                user.user_type = 3
                user.first_name = first_name
                user.last_name = last_name
                user.last_logout = datetime.now()
                user.save()

                user.students.address = address
                user.students.department_id = department
                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.save()


                # user = CustomUser.objects.create_user(username=username,
                #                                       password=password,
                #                                       email=email,
                #                                       first_name=first_name,
                #                                       last_name=last_name,
                #                                       user_type=3)
                # if department_id:
                #     department = Department.objects.get(id=department_id)
                #     user.students.department_id = department
                # user.students.address = address

                # course_obj = Courses.objects.get(id=course_id)
                # user.students.course_id = course_obj
                # if session_year_id:
                #     session_year_obj = SessionYearModel.objects.get(
                #         id=session_year_id)
                #     user.students.session_year_id = session_year_obj

                # user.students.gender = gender
                # user.students.profile_pic = profile_pic_url
                # user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                import traceback
                traceback.print_exc()
                messages.error(request, "Failed to Add Student.")
                return redirect('add_student')
        else:
            messages.error(
                request, "Failed to Add Student! errors:" + str(form.errors))
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):

    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()

    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    # form.fields['course_id'].initial = student.course_id and student.course_id.id or ""
    form.fields['gender'].initial = student.gender
    form.fields['department_id'].initial = student.department_id and student.department_id.id or ""
    # form.fields['session_year_id'].initial = student.session_year_id and student.session_year_id.id or ""

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            # course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            # session_year_id = form.cleaned_data['session_year_id']
            department_id = form.cleaned_data['department_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                if department_id:
                    department = Department.objects.get(id=department_id)
                    student_model.department_id = department
                student_model.address = address

                # course = Courses.objects.get(id=course_id)
                # student_model.course_id = course
                # if session_year_id:
                #     session_year_obj = SessionYearModel.objects.get(
                #         id=session_year_id)
                #     student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                import traceback
                traceback.print_exc()

                messages.error(request, "Failed to Update Student.")
                return redirect('/edit_student/'+student_id)
        else:

            messages.error(
                request, "Failed to Update Student, errors:" + str(form.errors))
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "staffs": staffs
    }
    return render(request, 'hod_template/add_subject_template.html', context)


def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)

        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name,
                               course_id=course,
                               staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff

            subject.save()

            messages.success(request, "Subject Updated Successfully.")

            return HttpResponseRedirect(reverse("edit_subject",
                                                kwargs={"subject_id": subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject",
                                                kwargs={"subject_id": subject_id}))


def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)


def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):

    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)
    attendance = Attendance.objects.filter(subject_id=subject_model,
                                           session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id,
                      "attendance_date": str(attendance_single.attendance_date),
                      "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data),
                        content_type="application/json",
                        safe=False)


@csrf_exempt
def admin_get_attendance_student(request):

    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name+" "+student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                # customuser.set_password(password)
                customuser.password = password
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')


# def staff_profile(request):
#     pass


# def student_profile(requtest):
#     pass


def add_campus(request):
    return render(request, "hod_template/add_campus_template.html")


def add_campus_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_campus')
    else:
        name = request.POST.get('name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        try:
            campus_model = Campuses(name=name,
                                    city=city,
                                    state=state)
            campus_model.save()
            messages.success(request, "Campus Added Successfully!")
            return redirect('add_campus')
        except:
            messages.error(request, "Failed to Add Campus!")
            return redirect('add_campus')


def manage_campus(request):
    campuses = Campuses.objects.all()
    context = {
        "campuses": campuses
    }
    return render(request, 'hod_template/manage_campus_template.html', context)


def edit_campus(request, campus_id):
    campus = Campuses.objects.get(id=campus_id)
    context = {
        "campus": campus,
        "id": campus_id
    }
    return render(request, 'hod_template/edit_campus_template.html', context)


def edit_campus_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')
        city = request.POST.get('city')
        state = request.POST.get('state')

        try:
            campus = Campuses.objects.get(id=id)
            campus.name = name
            campus.city = city
            campus.state = state
            campus.save()

            messages.success(request, "Campus Updated Successfully.")
            return redirect('/edit_campus/'+id)

        except:
            messages.error(request, "Failed to Update Campus.")
            return redirect('/edit_campus/'+id)


def delete_campus(request, campus_id):
    campus = Campuses.objects.get(id=campus_id)
    try:
        campus.delete()
        messages.success(request, "Campus Deleted Successfully.")
        return redirect('manage_campus')
    except:
        messages.error(request, "Failed to Delete Campus.")
        return redirect('manage_campus')


def add_classroom(request):
    form = AddClassroomForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_classroom_template.html', context)


def add_classroom_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_classroom')
    else:
        form = AddClassroomForm(request.POST, request.FILES)

        if form.is_valid():
            is_assigned = form.cleaned_data['is_assigned']
            campus_id = form.cleaned_data['campus_id']

            try:
                campus_obj = Campuses.objects.get(id=campus_id)
                classroom_model = Classrooms(is_assigned=is_assigned,
                                             campus_id=campus_obj)
                classroom_model.save()
                messages.success(request, "Classroom Added Successfully!")
                return redirect('add_classroom')
            except:
                messages.error(request, "Failed to Add Classroom!")
                return redirect('add_classroom')
        else:
            return redirect('add_classroom')


def manage_classroom(request):
    classrooms = Classrooms.objects.all()
    context = {
        "classrooms": classrooms
    }
    return render(request, 'hod_template/manage_classroom_template.html', context)


def edit_classroom(request, classroom_id):

    # Adding Classroom ID into Session Variable
    request.session['classroom_id'] = classroom_id

    classroom = Classrooms.objects.get(id=classroom_id)
    form = EditClassroomForm()

    # Filling the form with Data from Database
    form.fields['is_assigned'].initial = classroom.is_assigned
    form.fields['campus_id'].initial = classroom.campus_id.id

    context = {
        "id": classroom_id,
        "form": form
    }
    return render(request, "hod_template/edit_classroom_template.html", context)


def edit_classroom_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        classroom_id = request.session.get('classroom_id')
        if classroom_id == None:
            return redirect('/manage_classroom')

        form = EditClassroomForm(request.POST, request.FILES)
        if form.is_valid():
            is_assigned = form.cleaned_data['is_assigned']
            campus_id = form.cleaned_data['campus_id']

            try:
                # # First Update into Classroom Model
                # classroom = CustomUser.objects.get(id=classroom_id)
                # classroom.is_assigned = is_assigned
                # classroom.campus_id = campus_id
                # classroom.save()

                # Update Classroom Table
                classroom_model = Classrooms.objects.get(id=classroom_id)

                classroom_model.is_assigned = is_assigned

                campus = Campuses.objects.get(id=campus_id)
                classroom_model.campus_id = campus

                classroom_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['classroom_id']

                messages.success(request, "Classroom Updated Successfully!")
                return redirect('/edit_classroom/'+classroom_id)
            except:
                messages.success(request, "Failed to Uupdate Classroom.")
                return redirect('/edit_classroom/'+classroom_id)
        else:
            return redirect('/edit_classroom/'+classroom_id)


def delete_classroom(request, classroom_id):
    classroom = Classrooms.objects.get(id=classroom_id)
    try:
        classroom.delete()
        messages.success(request, "Classroom Deleted Successfully.")
        return redirect('manage_classroom')
    except:
        messages.error(request, "Failed to Delete Classroom.")
        return redirect('manage_classroom')

# def add_teacher(request):
#     return render(request, "hod_template/add_teacher_template.html")


def add_teacher(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'hod_template/add_teacher_template.html', context)


def add_teacher_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_teacher')
    else:
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)
        try:
            teacher_model = Teacher(
                name=name, department_id=department)
            teacher_model.save()
            messages.success(request, "Teacher Added Successfully!")
            return redirect('add_teacher')
        except:
            messages.error(request, "Failed to Add Teacher!")
            return redirect('add_teacher')

# def add_teacher_save(request):

#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('add_teacher')
#     else:
#         form = AddTeacherForm(request.POST, request.FILES)

#         if form.is_valid():
#             name = form.cleaned_data['Teacher Name']
#             department = form.cleaned_data['Department']

#             try:
#                 #teacher_obj = Teacher.objects.get(id=id)
#                 teacher_model = Teacher(name=name,
#                                              department=department)
#                 teacher_model.save()
#                 messages.success(request, "Teacher Added Successfully!")
#                 return redirect('add_teacher')
#             except:
#                 messages.error(request, "Failed to Add Teacher!")
#                 return redirect('add_teacher')
#         else:
#             messages.error(request, "empty")
#             return redirect('add_teacher')


def manage_teacher(request):
    teachers = Teacher.objects.all()

    context = {
        "teachers": teachers
    }
    return render(request, 'hod_template/manage_teacher_template.html', context)


def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    departments = Department.objects.all()
    context = {
        "teacher": teacher,
        "id": teacher_id,
        'departments': departments,
    }
    return render(request, 'hod_template/edit_teacher_template.html', context)


def edit_teacher_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        teacher_id = request.POST.get('id')
        name = request.POST.get('name')
        department_id = request.POST.get('department')

        department = Department.objects.get(id=department_id)
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.name = name
            teacher.department_id = department
            teacher.save()

            messages.success(request, "Teacher Updated Successfully.")
            return redirect('/edit_teacher/'+teacher_id)

        except:
            messages.error(request, "Failed to Update Teacher.")
            return redirect('/edit_teacher/'+teacher_id)


def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    try:
        teacher.delete()
        messages.success(request, "Teacher Deleted Successfully.")
        return redirect('manage_teacher')
    except:
        messages.error(request, "Failed to Delete Teacher.")
        return redirect('manage_teacher')


def add_department(request):
    return render(request, "hod_template/add_department_template.html")


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_department')
    else:
        name = request.POST.get('name')
        print(name)
        try:

            department_model = Department(
                name=name)
            print("1")
            department_model.save()
            print("2")
            messages.success(request, "Department Added Successfully!")
            return redirect('add_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('add_department')


def manage_department(request):
    departments = Department.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'hod_template/manage_department_template.html', context)


def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    context = {
        "department": department,
        "id": department_id
    }
    return render(request, 'hod_template/edit_department_template.html', context)


def edit_department_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')

        try:
            department = Department.objects.get(id=id)
            department.id = id
            department.name = name
            department.save()

            messages.success(request, "Department Updated Successfully.")
            return redirect('/edit_department/'+id)

        except:
            messages.error(request, "Failed to Update Campus.")
            return redirect('/edit_department/'+id)


def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "Department Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete Department.")
        return redirect('manage_department')
