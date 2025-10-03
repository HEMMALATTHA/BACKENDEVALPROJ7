from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee, Attendance, Payroll

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','phone','position','salary')
    search_fields = ('first_name','last_name','email','position')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id','employee','date','status')
    list_filter = ('status','date')
    search_fields = ('employee__first_name','employee__last_name')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('id','employee','month','year','working_days','present_days','salary_paid')
    list_filter = ('month','year')
