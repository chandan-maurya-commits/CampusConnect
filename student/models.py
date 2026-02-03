from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name  

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50) 

    def __str__(self):
        return f"{self.user.first_name}" 
    


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=20)
    
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)

    

    def __str__(self):
        return f"{self.user.first_name} ({self.get_year_display()})" 
    
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')  # Faculty user

    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    subject = models.CharField(max_length=100)
    assignment_number = models.IntegerField()
    description = models.TextField()
    due_date = models.DateField()
    file = models.FileField(upload_to='assignments/')
    created_by = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.assignment_number}"


class Club(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()

    coordinator_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to='club_logos/')

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    description = models.TextField()
    event_date = models.DateField()
    organizer_name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='event_posters/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
class PlacementDrive(models.Model):
    company_name = models.CharField(max_length=150)
    job_role = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    ctc = models.DecimalField(max_digits=5, decimal_places=2)  # LPA
    job_description = models.TextField()
    drive_date = models.DateField()
    last_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_role}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent')
        ]
    )

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject.name} ({self.subject.subject_code}) - {self.status}"
    
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.CharField(max_length=20)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField(default=100)

    class Meta:
        unique_together = ('student', 'subject', 'session')

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject.name}"

