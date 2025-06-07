from django.db import models
from datetime import date
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=100, default='Name')
    email = models.EmailField(unique=True, default='Email')
    phone_number = models.CharField(max_length=10, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],default='Other')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    password = models.CharField(max_length=28, default='Password')
    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.content:
            return f"{self.sender.name} to {self.receiver.name}: {self.content[:30]}"
        return f"{self.sender.name} to {self.receiver.name}: File"

class Status(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.FileField(upload_to='statuses/')
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.name} - {self.text[:30] if self.text else 'No Caption'}"
    def is_expired(self):
        return timezone.now() > (self.timestamp + timezone.timedelta(hours=24))