from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from .models import Campuses, CustomUser, Department, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult, Messages


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(
        student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj,
                                                         status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj,
                                                        status=False).count()
    #course_obj = Courses.objects.get(id=student_obj.course_id.id)
    #total_subjects = Subjects.objects.filter(course_id=course_obj).count()
    subject_name = []
    data_present = []
    data_absent = []
    messages = []
    if student_obj.admin.last_logout:
        messages = Messages.objects.filter(
            receiver_id=student_obj, created_at__gt=student_obj.admin.last_logout)

    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    # for subject in subject_data:
    #     attendance = Attendance.objects.filter(subject_id=subject.id)
    #     attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,
    #                                                                status=True,
    #                                                                student_id=student_obj.id).count()
    #     attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance,
    #                                                               status=False,
    #                                                               student_id=student_obj.id).count()
    #     subject_name.append(subject.subject_name)
    #     data_present.append(attendance_present_count)
    #     data_absent.append(attendance_absent_count)

    #     context = {
    #         "total_attendance": total_attendance,
    #         "attendance_present": attendance_present,
    #         "attendance_absent": attendance_absent,
    #         "total_subjects": total_subjects,
    #         "subject_name": subject_name,
    #         "data_present": data_present,
    #         "data_absent": data_absent,

    #     }

    context = {
        "messages": messages
    }

    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):

    # Getting Logged in Student Data
    student = Students.objects.get(admin=request.user.id)

    # Getting Course Enrolled of LoggedIn Student
    course = student.course_id

    # Getting the Subjects of Course Enrolled
    subjects = Subjects.objects.filter(course_id=course)
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(
            start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(
            end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)

        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)

        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date
        # Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,
                                                                       end_date_parse),
                                               subject_id=subject_obj)
        # Getting Attendance Report based on the attendance
        # details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                             student_id=stud_obj)

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)


def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj,
                                              leave_date=leave_date,
                                              leave_message=leave_message,
                                              leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj,
                                           feedback=feedback,
                                           feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    departments = Department.objects.all()
    campuses = Campuses.objects.all()
    context = {
        "user": user,
        "student": student,
        'departments': departments,
        'campuses': campuses,
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department_id = request.POST.get('department')
        campus_id = request.POST.get('campus')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                # customuser.set_password(password)
                customuser.password = password
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            if not student.campus:
                campus = Campuses.objects.get(id=campus_id)
                student.campus = campus
            if not student.department_id:
                department = Department.objects.get(id=department_id)
                student.department_id = department
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)


def student_view_registration(request):
    student = Students.objects.get(admin=request.user.id)
    courses = [student.course1, student.course2]
    context = {
        'status': student.is_approved,
        'courses': courses
    }
    return render(request, 'student_template/student_view_registration.html', context)


def student_register_course(request):
    all_courses = Courses.objects.all()
    student = Students.objects.get(admin=request.user.id)
    # all_courses = Courses.objects.filter(campus_id=student.campus)
    registration = [student.course1, student.course2]
    context = {
        "all_courses": all_courses,
        'registration': registration
    }
    return render(request, 'student_template/student_register_course.html', context)


# def student_register_course_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method.")
#         return redirect('student_register_course')
#     else:
#         course_id1 = request.POST.get('course1')
#         course_id2 = request.POST.get('course2')
#         student_obj = Students.objects.get(admin=request.user.id)
#         course1 = Courses.objects.get(id=course_id1)
#         course2 = Courses.objects.get(id=course_id2)

#         try:
#             student_obj.course1 = course1
#             student_obj.course2 = course2
#             student_obj.save()
#             messages.success(request, "Successfully registered!")
#             return redirect('student_register_course')
#         except:
#             messages.error(request, "Failed to register!")
#             return redirect('student_register_course')


def student_add_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    student = Students.objects.get(admin=request.user.id)
    # check if student has registered this course
    if course == student.course1 or course == student.course2:
        messages.error(request, "You have registered this course!")
    # check if student can register one more course
    elif student.course1 and student.course2:
        messages.error(
            request,
            'You can register at most 2 courses. You have reached the limit!')
    # check the course's capacity
    elif course.capacity <= course.curr_num_of_students:
        messages.error(request, 'This course has no seat!')
    else:
        if not student.course1:
            student.course1 = course
        else:
            student.course2 = course
        student.is_approved = None
        student.save()
        course.curr_num_of_students += 1
        course.save()
        messages.success(
            request, 'Successfully registered! Your registration status was reset to Pending.')
    return redirect('student_register_course')


def student_drop_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    student = Students.objects.get(admin=request.user.id)
    if course != student.course1 and course != student.course2:
        messages.error(request, 'Failed to drop this course!')
    else:
        if course == student.course1:
            student.course1 = None
        elif course == student.course2:
            student.course2 = None
        student.is_approved = None
        student.save()
        course.curr_num_of_students -= 1
        course.save()
        messages.success(
            request, 'Successfully dropped. Your registration status was reset to Pending.')
    return redirect('student_register_course')
