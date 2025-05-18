from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeeForm
from .models import Employee, Attendance
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from io import BytesIO
import calendar

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'attendance/login.html')

# Create your views here.
@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        messages.info(request, "Session expired. Please log in again.")
    return render(request, 'attendance/home.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def mark_attendance(request):
    employees = Employee.objects.all()
    return render(request, 'attendance/mark_attendance.html', {'employees': employees})

@login_required(login_url='login')
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('add_employee')
    else:
        form = EmployeeForm()

    return render(request, "attendance/add_employee.html", {"form": form})

@login_required(login_url='login')
def submit_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        employee_id = request.POST.get('employee_name')
        attendance_status = request.POST.get('attendance_status')
        task = request.POST.get('task', '')

        try:
            employee = Employee.objects.get(id=employee_id)
            attendance = Attendance(
                employee=employee,
                date=date,
                attendance_status=attendance_status,
                task=task
            )
            attendance.save()
            messages.success(request, 'Attendance submitted successfully!')
        except Employee.DoesNotExist:
            messages.error(request, 'Selected employee does not exist.')

        return redirect('mark_attendance')

    return redirect('mark_attendance')

@login_required(login_url='login')
def show_summary_selector(request):
    # Render the main summary page with buttons
     return render(request, 'attendance/show_summary.html')

@login_required(login_url='login')
def download_employee_pdf(request):
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employee_sheet.pdf"'

    # Create a PDF object
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    pdf.setTitle("Employee Sheet")

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2.0, height - 50, "Employee Sheet")

    # Fetch employee data
    employees = Employee.objects.all()

    # Table data: header row + employee rows
    data = [['Sr No', 'Name', 'Contact Number', 'Address']]
    for i, emp in enumerate(employees, start=1):
        data.append([str(i), emp.name, emp.contact_number, emp.address])

    # Create table
    table = Table(data, colWidths=[50, 150, 150, 150])

    # Style the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Calculate position to draw the table (from bottom left)
    table_width, table_height = table.wrap(0, 0)
    x = (width - table_width) / 2
    y = height - 100 - table_height

    # Draw table on PDF
    table.drawOn(pdf, x, y)

    # Finalize the PDF
    pdf.showPage()
    pdf.save()

    return response

@login_required(login_url='login')
def select_attendance(request):
    months = [datetime(2025, i, 1).strftime('%B') for i in range(1, 13)]
    employees = Employee.objects.all()
    return render(request, 'attendance/attendance_selection.html', {'employees': employees, 'months': months})

@login_required(login_url='login')
def download_attendance_pdf(request):
    employee_id = request.GET.get('employee_id')
    month = request.GET.get('month')

    employee = get_object_or_404(Employee, id=employee_id)
    month_index = datetime.strptime(month, "%B").month
    year = datetime.now().year  # or customize if needed

    # Prepare a date -> record dict for easy lookup
    records = Attendance.objects.filter(
        employee=employee,
        date__month=month_index
    )
    record_dict = {a.date: a for a in records}

    # Get all dates in month
    num_days = calendar.monthrange(year, month_index)[1]
    all_dates = [datetime(year, month_index, day).date() for day in range(1, num_days + 1)]

    # PDF setup
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    # Employee Info
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, y, f"Employee: {employee.name}")
    p.setFont("Helvetica", 12)
    y -= 20
    p.drawString(40, y, f"Contact: {employee.contact_number}")
    y -= 20
    p.drawString(40, y, f"Address: {employee.address}")
    y -= 20
    p.drawString(40, y, f"Month: {month}")
    y -= 30

    # Table Headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Date")
    p.drawString(150, y, "Status")
    p.drawString(270, y, "Task")
    y -= 20

    # Table Content
    p.setFont("Helvetica", 11)
    present = absent = unassigned = 0

    for date in all_dates:
        record = record_dict.get(date)
        status = record.attendance_status if record else "Unassigned"
        task = record.task if record and record.task else "-"

        # Count summary
        if status == "Present":
            present += 1
        elif status == "Absent":
            absent += 1
        else:
            unassigned += 1

        # Draw row
        p.drawString(40, y, date.strftime("%Y-%m-%d"))
        p.drawString(150, y, status)
        p.drawString(270, y, task)

        y -= 20
        if y < 60:
            p.showPage()
            y = height - 50

    # Summary
    y -= 20
    if y < 100:
        p.showPage()
        y = height - 50

    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Summary")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Total Present Days: {present}")
    y -= 20
    p.drawString(40, y, f"Total Absent Days: {absent}")
    y -= 20
    p.drawString(40, y, f"Total Unassigned Days: {unassigned}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
 
@login_required(login_url='login')
def summary_selection(request):
    # Just render the menu page with buttons
    return render(request, 'attendance/show_summary.html')

@login_required(login_url='login')
def show_summary(request, summary_type):
    # You can handle logic here based on summary_type (attendance or employeesheet)
    if summary_type == "attendance":
        # Redirect or render attendance related page
        return redirect('select_attendance')
    elif summary_type == "employeesheet":
        # Redirect or render employee sheet page or directly download PDF
        return redirect('download_employee_pdf')
    else:
        # Handle unknown summary_type gracefully
        return render(request, 'attendance/404.html', status=404)
    