from cProfile import Profile
from django.http import HttpResponse
# from django.http import HttpResponseForbidden
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils.timezone import now
from .models import Student, Faculty
from .models import Subject
from .models import Assignment
from .models import Club
from .models import Event
from .models import PlacementDrive
from .models import Student , Profile , Result
from .models import Attendance
from django.contrib.auth.decorators import login_required
import csv


def index(request):
    return render(request, 'index.html')


def logout(request):
    return render(request, 'log.html') 

def clubs(request):
    clubs = Club.objects.all()   # fetch all clubs
    return render(request, 'clubs.html', {
        'clubs': clubs
    }) 


@login_required(login_url='log')
def events_form(request):
    return render(request, 'events_form.html')


@login_required(login_url='log')
def placements(request):   
    return render(request, 'placements.html')


@login_required(login_url='log')
def event_registration(request):
    return render(request, 'event_registration.html')


@login_required(login_url='log')
def placement_apply(request):
    return render(request, 'placement_apply.html') 

@login_required(login_url='log')
def base(request):
    return render(request, 'base.html') 


@login_required(login_url='log')
def place_form(request):
    return render(request , 'place_form.html')


# Registration
def register_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        department = request.POST.get("department")
        subject_code = request.POST.get('subject_code')
        roll_no = request.POST.get('roll_no')
        year = request.POST.get("year")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password
        )
        
        Profile.objects.create(
            user=user,
            role=role,
            department=department
        )

        if role == "Student":
            Student.objects.create(
                user=user,
                name=name,          # ✅ FIX
                department=department,
                roll_no=roll_no,
                year=year           # ✅ FIX
            )

        elif role == "Coordinator":
            faculty = Faculty.objects.create(
                user=user,
                department=department
            )

            SUBJECT_MAP = {
                "ML-101": "Machine Learning",
                "DA-102": "Data Analytics",
                "DAA-103": "Design & Analysis of Algorithms",
                "WT-104": "Web Technology",
                "ITCS-105": "ITCS",
                "DBMS-106": "Database Management System",
            }

            if subject_code:

                Subject.objects.create(
                    name=request.POST.get('name'),
                    subject_code=subject_code,
                    faculty=request.user
)

        messages.success(request, "Registration successful! Please login.")
        return redirect("log")

    return render(request, "reg.html")



# Login
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("log") 

        login(request, user)

        # ✅ ROLE DETECTION (CORRECT)
        if hasattr(user, "student"):
            return redirect("student_dashboard")

        elif hasattr(user, "faculty"):
            return redirect("coordinator_dashboard")

        else:
            messages.error(request, "Role not assigned")
            return redirect("log")

    return render(request, "log.html") 


@login_required(login_url='log')
def coordinator_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        messages.error(request, "Access denied. You are not a coordinator.")
        return redirect('log') 

    faculty = Faculty.objects.get(user=request.user)

    # ✅ Subjects taught by this faculty
    subjects = Subject.objects.filter(faculty=request.user)

    # ✅ Profile (safe way)
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={ 
            "role": "Faculty",
            "department": faculty.department
        }
    )  

    assignments = Assignment.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    clubs = Club.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    events = Event.objects.filter(created_by=request.user).order_by('-created_at')
    placements = PlacementDrive.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, "coordinator_dashboard.html", {
        "faculty": faculty,
        "subjects": subjects,
        "assignments": assignments,
        "clubs": clubs,
        "placements": placements,   # ✅ ADDED
        "events": events,
        "profile": profile,# ✅ ADDED
    })





    
    # return render(request, 'student_dashboard.html', {'std_name': std_name} )



@login_required(login_url='log')
def assignment_form(request):
    return render(request, 'assignment_form.html')

@login_required(login_url='log')
def base2(request):
    return render(request, 'base2.html') 

# def club_form(request):
#     return render(request, 'club_form.html')
@login_required(login_url='log')
def add_assignment(request):
    if request.method == "POST":
        Assignment.objects.create(
            subject=request.POST.get('subject'),
            assignment_number=request.POST.get('assignment_number'),
            description=request.POST.get('description'),
            due_date=request.POST.get('due_date'),
            file=request.FILES.get('file'),
            created_by=request.user   # 🔥 important
        )
        return redirect('coordinator_dashboard')

    return render(request, 'assignment.html')


@login_required(login_url='log')
def club_form(request): 
    return render(request, 'club_form.html')

@login_required(login_url='log')
def add_club(request):
    if request.method == "POST": 
        Club.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            coordinator_name=request.POST.get('coordinator_name'),
            contact_email=request.POST.get('contact_email'),
            logo=request.FILES.get('logo'),
            created_by=request.user
        )

        messages.success(request, "Club created successfully!")
        return redirect('coordinator_dashboard')

    return render(request, 'club_form.html') 
    
@login_required(login_url='log')
def add_event(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('descrip')
        date = request.POST.get('date')
        organizer = request.POST.get('org_name')
        poster = request.FILES.get('up_poster')
        

        if not poster:
            messages.error(request, "Please upload an event poster.")
            return redirect('add_event')

        Event.objects.create(
            title=title,
            category=category,
            description=description,
            event_date=date,
            organizer_name=organizer,
            poster=poster,
            created_by=request.user
        )

        messages.success(request, "Event created successfully!")
        return redirect('coordinator_dashboard')

    return render(request, 'add_event.html')

@login_required(login_url='log')
def add_placement_drive(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        job_role = request.POST.get('job_role')
        eligibility = request.POST.get('eligibility')
        ctc = request.POST.get('ctc')
        job_description = request.POST.get('job_description')
        drive_date = request.POST.get('drive_date')
        last_date = request.POST.get('last_date')

        PlacementDrive.objects.create(
            company_name=company_name,
            job_role=job_role,
            eligibility=eligibility,
            ctc=ctc,
            job_description=job_description,
            drive_date=drive_date,
            last_date=last_date,
            created_by=request.user
        )

        messages.success(request, "Placement drive created successfully 🎉")
        return redirect('add_placement_drive')  # or dashboard/list page

    return render(request, 'place_form.html')


@login_required(login_url='log')
def std_assignment(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return redirect('log')  # user is not a student

    assign = Assignment.objects.filter(
        created_by__faculty__department=student.department
    )

    return render(request, 'std_assignment.html', {"assign": assign})

@login_required(login_url='log')
def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {
        'events': events
    })
    

@login_required(login_url='log')
def placements(request):
    placements = PlacementDrive.objects.all()
    return render(request , 'placements.html' , {'placements':placements}) 

@login_required(login_url='log')
def profile(request):
    user = request.user

    # Get profile
    profile = Profile.objects.get(user=user)

    # Counts
    assignments_count = Assignment.objects.filter(created_by=user).count()
    clubs_count = Club.objects.filter(created_by=user).count()
    events_count = Event.objects.filter(created_by=user).count()
    placements_count = PlacementDrive.objects.filter(created_by=user).count()

    context = {
        "user": user,
        "profile": profile,
        "assignments_count": assignments_count,
        "clubs_count": clubs_count,
        "events_count": events_count,
        "placements_count": placements_count,
    }

    return render(request, "profile.html", context) 

@login_required(login_url='log')
def about(request):
    return render(request , 'about.html')

@login_required(login_url='log')
def lout(request):
    return render(request , 'log.html')


@login_required(login_url='log')
def student_dashboard(request):
    user = request.user
    std_name = Student.objects.all()
    student = Student.objects.filter(user=user).first()
    profile = Profile.objects.filter(user=user).first()
    
    if not student:
        messages.error(request, "Student profile not found.")
        return redirect("log")

    today = now().date()

    assignments_today = Assignment.objects.filter(
        created_at__date=today,
        created_by__profile__department=student.department
    ).count()

    clubs_today = Club.objects.filter(
        created_at__date=today
    ).count()

    events_today = Event.objects.filter(
        created_at__date=today
    ).count()

    placements_today = PlacementDrive.objects.filter(
        created_at__date=today
    ).count()


    return render(request, 'student_dashboard.html', {'std_name':std_name, "student": student , "profile": profile,"assignments_today": assignments_today,
        "clubs_today": clubs_today,
        "events_today": events_today,
        "placements_today": placements_today,})



from django.utils.timezone import now
@login_required(login_url='log')
def st_profile(request):
    user = request.user

    profile = Profile.objects.filter(user=user).first()
    student = Student.objects.filter(user=user).first()

    if not student:
        messages.error(request, "Student profile not found.")
        return redirect("log")

    today = now().date()

    assignments_today = Assignment.objects.filter(
        created_at__date=today,
        created_by__profile__department=student.department
    ).count()

    clubs_today = Club.objects.filter(
        created_at__date=today
    ).count()

    events_today = Event.objects.filter(
        created_at__date=today
    ).count()

    placements_today = PlacementDrive.objects.filter(
        created_at__date=today
    ).count()

    return render(request, "st_profile.html", {
        "user": user,
        "profile": profile,        # may be None, template-safe
        "student": student,        # contains year, roll_no, name
        "assignments_today": assignments_today,
        "clubs_today": clubs_today,
        "events_today": events_today,
        "placements_today": placements_today,
    })



import csv
from django.http import HttpResponse
from student.models import Student, Subject, Attendance
@login_required(login_url='log')
def upload_attendance(request):
    if request.method == "POST":

        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return HttpResponse("No file uploaded")

        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        saved = 0

        for row in reader:
            roll_no = row.get('roll_no', '').strip()
            subject_name = row.get('subject', '').strip()
            status = row.get('status', '').strip()

            try:
                student = Student.objects.get(roll_no=roll_no)
                subject = Subject.objects.get(name__iexact=subject_name)

                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    status=status
                )

                saved += 1

            except Student.DoesNotExist:
                print(f"❌ Student not found: {roll_no}")

            except Subject.DoesNotExist:
                print(f"❌ Subject not found: {subject_name}")

            except Exception as e:
                print("🔥 ERROR:", e)

        return HttpResponse(f"✅ Attendance uploaded: {saved}")

    return render(request, 'upload_attendance.html')


@login_required(login_url='log')
def upload_results(request):
    faculty = request.user

    # Only subjects assigned to this faculty
    subjects = Subject.objects.filter(faculty=faculty)

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        session = request.POST.get('session')
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            return HttpResponse("CSV file missing")

        # 🔐 SECURITY: faculty can upload only their subject
        subject = Subject.objects.filter(
            name=subject_name,
            faculty=faculty
        ).first()

        if not subject:
            return HttpResponse("Unauthorized subject", status=403)

        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            roll_no = row['roll_no'].strip()
            marks = int(row['marks'])

            student = Student.objects.filter(roll_no=roll_no).first()
            if not student:
                continue

            Result.objects.update_or_create(
                student=student,
                subject=subject,
                session=session,
                defaults={
                    'marks_obtained': marks,
                    'total_marks': 100
                }
            )

        return redirect('upload_results')

    return render(request, 'upload_results.html', {
        'subjects': subjects
    })


 






@login_required(login_url='log')
def student_attendance(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "student_attendance.html", {
            "attendance": [],
        })

    attendance = Attendance.objects.filter(
        student=student
    ).select_related("subject")

    return render(request, "student_attendance.html", {
        "attendance": attendance
    })

@login_required(login_url='log')
def results(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'results.html', {
            'error': 'Student profile not linked with this account.'
        })

    results = Result.objects.filter(student=student)

    return render(request, 'results.html', {
        'student': student,
        'results': results
    })