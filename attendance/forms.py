from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        label='Username', 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    

class StudentRegisterForm(UserCreationForm):
    name = forms.CharField(
        max_length=255,
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    roll_number = forms.CharField(
        max_length=20,
        label='Roll Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your roll number'})
    )
    image = forms.ImageField(
        label='Upload Image',
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'name', 'roll_number', 'image', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                roll_number=self.cleaned_data['roll_number'],
                image=self.cleaned_data['image']
            )
        return user

   