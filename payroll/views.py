from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Employee, Attendance, Payroll
from .forms import EmployeeForm, AttendanceForm
import pandas as pd
from reportlab.pdfgen import canvas
import io
from datetime import datetime, date
from django.db.models import Sum

# Employee Views
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'payroll/employee_list.html', {'employees': employees})

def employee_add(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'payroll/employee_form.html', {'form': form})

def employee_edit(request, pk):
    emp = Employee.objects.get(id=pk)
    form = EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'payroll/employee_form.html', {'form': form})

def employee_delete(request, pk):
    Employee.objects.get(id=pk).delete()
    return redirect('employee_list')

# Attendance Views
def attendance_list(request):
    attendance = Attendance.objects.select_related('employee').all().order_by('-date')
    return render(request, 'payroll/attendance_list.html', {'attendances': attendance})

def attendance_add(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('attendance_list')
    return render(request, 'payroll/attendance_form.html', {'form': form})

# Payroll Views
def generate_payroll(request, month, year):
    """
    Generate payrolls for a given month/year.
    - If payroll exists, do not overwrite (preserve Admin edits).
    - If payroll does not exist, calculate and create it.
    """
    for emp in Employee.objects.all():
        total_days = Attendance.objects.filter(employee=emp, date__month=month, date__year=year).count()
        present_days = Attendance.objects.filter(employee=emp, date__month=month, date__year=year, status='Present').count()
        salary_per_day = emp.salary / total_days if total_days else emp.salary
        salary_paid = salary_per_day * present_days

        # Create payroll only if not exists (preserve Admin edits later)
        Payroll.objects.get_or_create(
            employee=emp,
            month=month,
            year=year,
            defaults={
                'working_days': total_days,
                'present_days': present_days,
                'salary_paid': salary_paid
            }
        )

    # Fetch all payrolls for report
    payrolls = Payroll.objects.filter(month=month, year=year).select_related('employee')
    return render(request, 'payroll/payroll_report.html', {
        'payrolls': payrolls,
        'month': month,
        'year': year
    })

def payroll_export_excel(request, month, year):
    payrolls = Payroll.objects.filter(month=month, year=year)
    data = [[p.employee.first_name, p.employee.last_name, p.working_days, p.present_days, float(p.salary_paid)] for p in payrolls]
    df = pd.DataFrame(data, columns=['First Name','Last Name','Working Days','Present Days','Salary Paid'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Payroll_{month}_{year}.xlsx'
    df.to_excel(response, index=False)
    return response

def payroll_export_pdf(request, month, year):
    payrolls = Payroll.objects.filter(month=month, year=year)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, f"Payroll Report {month}/{year}")
    y -= 30
    p.setFont("Helvetica", 12)
    for pay in payrolls:
        p.drawString(50, y, f"{pay.employee.first_name} {pay.employee.last_name} - Salary Paid: {pay.salary_paid}")
        y -= 20
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def dashboard(request):
    today = date.today()
    month = today.month
    year = today.year

    total_employees = Employee.objects.count()
    present_today = Attendance.objects.filter(date=today, status='Present').count()
    total_salary = Payroll.objects.filter(month=month, year=year).aggregate(total=Sum('salary_paid'))['total'] or 0

    context = {
        'total_employees': total_employees,
        'present_today': present_today,
        'total_salary': total_salary,
        'today': today,
        'month': month,
        'year': year,
    }
    return render(request, 'payroll/dashboard.html', context)
