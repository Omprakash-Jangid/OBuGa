from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),    # /login/
    path('home/', views.home, name='home'),            # /home/
    path('logout/', views.logout_view, name='logout'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('show_summary/', views.show_summary_selector, name='show_summary_selector'),
    path('summary/', views.summary_selection, name='summary'),
    path('show_summary/<str:summary_type>/', views.show_summary, name='show_summary'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('download_employee_pdf/', views.download_employee_pdf, name='download_employee_pdf'),
    path('select_attendance/', views.select_attendance, name='select_attendance'),
    path('download_attendance_pdf/', views.download_attendance_pdf, name='download_attendance_pdf'),
]


