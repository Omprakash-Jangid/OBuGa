from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Unassigned', 'Unassigned'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    attendance_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    task = models.TextField(blank=True, null=True) 
    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.attendance_status}"