from django import forms
from .models import Courses, SessionYearModel, Campuses, Department


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Campuses
    try:
        campuses = Campuses.objects.all()
        campuses_list = []
        for campus in campuses:
            single_campus = (campus.id, campus.name)
            campuses_list.append(single_campus)
    except:
        campuses_list = []

    campuses_id = forms.ChoiceField(label="Campus",
                                    choices=campuses_list,
                                    widget=forms.Select(attrs={"class": "form-control"}))

    try:
        departments = Department.objects.all()
        departments_list = []
        for department in departments:
            single_department = (department.id, department.name)
            departments_list.append(single_department)
    except:
        print("here")
        departments_list = []

    department_id = forms.ChoiceField(choices=departments_list, label="Department",
                                      widget=forms.Select(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # course_id = forms.ChoiceField(label="Course",
    #                               choices=course_list,
    #                               widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    # session_year_id = forms.ChoiceField(label="Session Year",  required=False,
    # 									choices=session_year_list,
    # 									widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Campuses
    try:
        campuses = Campuses.objects.all()
        campuses_list = []
        for campus in campuses:
            single_campus = (campus.id, campus.name)
            campuses_list.append(single_campus)
    except:
        campuses_list = []

    campuses_id = forms.ChoiceField(label="Campus",
                                    choices=campuses_list,
                                    widget=forms.Select(attrs={"class": "form-control"}))

    try:
        departments = Department.objects.all()
        departments_list = []
        for department in departments:
            single_department = (department.id, department.name)
            departments_list.append(single_department)
    except:
        print("here")
        departments_list = []

    department_id = forms.ChoiceField(choices=departments_list, label="Department",
                                      widget=forms.Select(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # course_id = forms.ChoiceField(label="Course",
    #                               choices=course_list,
    #                               widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    # session_year_id = forms.ChoiceField(label="Session Year", required=False,
    #                                     choices=session_year_list,
    #                                     widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class AddClassroomForm(forms.Form):
    is_assigned_list = (
        ('true', 'true'),
        ('false', 'false')
    )

    # For Displaying Campuses
    try:
        campuses = Campuses.objects.all()
        campus_list = []
        for campus in campuses:
            single_campus = (campus.id, campus.name)
            campus_list.append(single_campus)
    except:
        print("here")
        campus_list = []

    is_assigned = forms.ChoiceField(label="Is Assigned",
                                    choices=is_assigned_list,
                                    widget=forms.Select(attrs={"class": "form-control"}))

    campus_id = forms.ChoiceField(label="Campus",
                                  choices=campus_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class EditClassroomForm(forms.Form):
    is_assigned_list = (
        ('true', 'true'),
        ('false', 'false')
    )

    # For Displaying Campuses
    try:
        campuses = Campuses.objects.all()
        campus_list = []
        for campus in campuses:
            single_campus = (campus.id, campus.name)
            campus_list.append(single_campus)
    except:
        print("here")
        campus_list = []

    is_assigned = forms.ChoiceField(label="Is Assigned",
                                    choices=is_assigned_list,
                                    widget=forms.Select(attrs={"class": "form-control"}))

    campus_id = forms.ChoiceField(label="Campus",
                                  choices=campus_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class AddTeacherForm(forms.Form):
    name = forms.CharField(label="Teacher Name",
                           max_length=50,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.CharField(label="Department",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))


class AddDepartmentForm(forms.Form):
    id = forms.CharField(label="Department Id",
                         max_length=50,
                         widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="Department Name",
                           max_length=50,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
