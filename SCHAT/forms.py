from django import forms
from .models import Student
from .models import Status



class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone_number', 'gender', 'dob', 'photo','password']
        labels = {
            'name': 'name',
            'email': 'email',
            'mobile_number': 'mobile_number',
            'gender': 'gender',
            'dob': 'dob',
            'photo': 'photo',
            'password': 'password',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter your email'})
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter your password'})
    )


class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Student
        exclude = ['phone_number', 'password']
        fields = ['name', 'email', 'dob', 'phone_number', 'gender', 'photo', 'password']

class PasswordResetForm(forms.Form):
        email = forms.EmailField()
        dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)))

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['content','text']