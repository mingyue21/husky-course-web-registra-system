from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#from django_mysql.models import ListCharField
import json


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    # HOD = '1'
    # STAFF = '2'
    # STUDENT = '3'

    # EMAIL_TO_USER_TYPE_MAP = {
    # 	'hod': HOD,
    # 	'staff': STAFF,
    # 	'student': STUDENT
    # }

    # user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Student"))

    ADMIN = '1'
    ADVISOR = '2'
    STUDENT = '3'

    EMAIL_TO_USER_TYPE_MAP = {
        'admin': ADMIN,
        'advisor': ADVISOR,
        'student': STUDENT
    }

    user_type_data = ((ADMIN, "Admin"), (ADVISOR, "Advisor"),
                      (STUDENT, "Student"))

    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)

    last_logout = models.DateTimeField(blank=True, null=True)


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    objects = models.Manager()


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department_id = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True)
    department_id = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    department_id = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    #teacherCourses = ListCharField(base_field=CharField(max_length=10))()
    objects = models.Manager()

    # to get a list of courses
    # teachingCourses = models.CharField(max_length=200)

    # def set_teachingCourses(self, x):
    #     self.teachingCourses = json.dumps(x)

    # def get_teachingCourses(self):
    #     return json.loads(self.teachingCourses)


class Campuses(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    objects = models.Manager()


class Classrooms(models.Model):
    id = models.AutoField(primary_key=True)
    is_assigned = models.CharField(max_length=10)
    campus_id = models.ForeignKey(Campuses, on_delete=models.CASCADE)
    objects = models.Manager()


class InstructionalMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    objects = models.Manager()


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    campus_id = models.ForeignKey(
        Campuses, on_delete=models.CASCADE, null=True)
    teacher_id = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True)
    classroom_id = models.ForeignKey(
        Classrooms, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(default=30)
    curr_num_of_students = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructional_method = models.ForeignKey(
        InstructionalMethod, on_delete=models.DO_NOTHING, null=True)
    day = models.CharField(max_length=30, null=True)
    time = models.TimeField(null=True)
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    # need to give default course
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department_id = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(
        Courses, on_delete=models.DO_NOTHING, null=True)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,
                                        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course1 = models.ForeignKey(
        Courses, on_delete=models.DO_NOTHING, null=True, related_name='course1_set')
    course2 = models.ForeignKey(
        Courses, on_delete=models.DO_NOTHING, null=True, related_name='course2_set')
    is_approved = models.BooleanField(null=True)
    campus = models.ForeignKey(
        Campuses, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()


class Attendance(models.Model):

    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Creating Django Signals
@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will
# automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:

        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance,
                                    # course_id=Courses.objects.get(id=1),
                                    # session_year_id=SessionYearModel.objects.get(
                                    #     id=1),
                                    address="",
                                    profile_pic="",
                                    gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
