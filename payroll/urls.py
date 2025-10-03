from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard homepage

    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),

    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),

    path('payroll/<int:month>/<int:year>/', views.generate_payroll, name='generate_payroll'),
    path('payroll/excel/<int:month>/<int:year>/', views.payroll_export_excel, name='payroll_export_excel'),
    path('payroll/pdf/<int:month>/<int:year>/', views.payroll_export_pdf, name='payroll_export_pdf'),
]
