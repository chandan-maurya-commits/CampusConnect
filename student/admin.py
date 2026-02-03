from django.contrib import admin
from .models import Profile , Student, Faculty , Subject  , Assignment , Club , Event , PlacementDrive , Attendance , Result

# Register your models here.

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Profile) 
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(PlacementDrive)
admin.site.register(Attendance)
admin.site.register(Result)

