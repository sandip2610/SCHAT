from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import LoginForm, EditProfileForm, PasswordResetForm
from .models import Student, Message
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
import random
from django.contrib import messages
from .models import Status
from django.utils import timezone
from datetime import timedelta
import requests
import urllib.parse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import StatusForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        dob = request.POST.get('dob', '').strip()
        gender = request.POST.get('gender', '').strip()
        password = request.POST.get('password', '').strip()
        photo = request.FILES.get('photo')
        if not all([name, email, phone_number, dob, gender, password, photo]):
            messages.error(request, 'Please fill all the required fields.')
            return render(request, 'register.html')
        # Check if email already exists
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered. Please use a different one.')
            return render(request, 'register.html')
        student = Student(
            name=name,
            email=email,
            phone_number=phone_number,
            gender=gender,
            dob=dob,
            password=password,  # Consider using hashed password!
            photo=photo
        )
        student.save()
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'register.html')

def student_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                student = Student.objects.get(email=email, password=password)
                request.session['student_id'] = student.id
                return redirect('chat_board')
            except Student.DoesNotExist:
                return render(request, 'login.html', {'form': form, 'error': 'Email or Password is Wrong!'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']
            try:
                student = Student.objects.get(email=email, dob=dob)
                temp_password = str(random.randint(100000, 999999))
                student.password = temp_password
                student.save()
                send_mail(
                    'Temporary Password',
                    f'Your temporary password is: {temp_password}. Please log in and change your password.',
                    'your_email@example.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'password_reset.html',
                              {'form': form, 'success': 'A temporary password has been sent to your email.'})
            except Student.DoesNotExist:
                return render(request, 'password_reset.html',
                              {'form': form, 'error': 'Invalid email or date of birth.'})
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        student_id = request.session.get('student_id')
        if student_id:
            student = Student.objects.get(id=student_id)
            if student.password != old_password:
                messages.error(request, 'Old password does not match.')
                return render(request, 'change_password.html')
            if new_password != confirm_password:
                messages.error(request, 'New password and confirm password do not match.')
                return render(request, 'change_password.html')
            student.password = new_password
            student.save()
            messages.success(request, 'Password changed successfully. Please log in again.')
            return redirect('login')
        else:
            messages.error(request, 'User not logged in.')
            return redirect('login')
    return render(request, 'change_password.html')

def profile(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('login')
    return render(request, 'profile.html', {'student': student})

def chat_board(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    receiver_id = request.GET.get('receiver_id')

    if receiver_id:
        receiver = Student.objects.get(id=receiver_id)
    else:
        receiver = None
    if request.method == "POST":
        content = request.POST.get('content')
        uploaded_file = request.FILES.get('file')
        receiver_id = request.POST.get('receiver_id')
        receiver = Student.objects.get(id=receiver_id)
        if content or uploaded_file:
            message = Message.objects.create(sender=student, receiver=receiver, content=content)
            if uploaded_file:
                message.file = uploaded_file
                message.save()
        return redirect(f'{request.path}?receiver_id={receiver_id}')

    # Use Q objects for complex queries
    messages = Message.objects.filter(
        Q(sender=student, receiver=receiver) | Q(sender=receiver, receiver=student)
    ).order_by('timestamp')
    students = Student.objects.exclude(id=student_id)
    return render(request, 'chat_board.html', {
        'messages': messages,
        'students': students,
        'receiver': receiver,
    })

def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == "POST":
        new_content = request.POST.get('new_content')
        message.content = new_content
        message.save()
    return redirect('chat_board')

def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return redirect('chat_board')

def upload_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.save(commit=False)
            student_id = request.session.get('student_id')
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                    status.student = student
                    status.save()
                    return redirect('all_statuses')
                except Student.DoesNotExist:
                    messages.error(request, 'Account not found.')
                    return redirect('chat_board')
            else:
                messages.error(request, 'You are not logged in.')
                return redirect('chat_board')
    else:
        form = StatusForm()
    return render(request, 'upload_status.html', {'form': form})

def all_statuses(request):
    time_threshold = timezone.now() - timedelta(hours=24)
    statuses = Status.objects.filter(timestamp__gte=time_threshold).order_by('-timestamp')
    return render(request, 'all_statuses.html', {'statuses': statuses})

def delete_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    student_id = request.session.get('student_id')
    if student_id and status.student.id == student_id:
        status.delete()
        messages.success(request, 'The status has been successfully deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this status.')
    return redirect('all_statuses')

def san(request):
    return render(request, 'san.html')

def edit_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=student)
    return render(request, 'edit_profile.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')

def video_call(request, room_name):
    return render(request, 'chat_board.html', {'room_name': room_name})

def search_page(request):
    return render(request, 'search.html')

def google_search(query):
    API_KEY = 'AIzaSyCZXPzwpbBGCF8b6jWgVTjhO75Z6v_1cfo'
    CX = '42c378d6f4c234f98'
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={API_KEY}&cx={CX}"
    response = requests.get(url)
    try:
        data = response.json()
        print("Full response:", data)
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['snippet']
        else:
            return "I couldn't find any information about that....."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_search_result(request):
    user_query = request.GET.get('query', '')
    result = google_search(user_query)
    return JsonResponse({'reply': result})