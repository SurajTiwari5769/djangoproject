from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name', 'required': 'required'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name', 'required': 'required'}),
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username', 'required': 'required'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'required': 'required'}),
    )
    password1 = forms.CharField(
        label = 'Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password', 'required': 'required'})
    )
    password2 = forms.CharField(
        label = 'Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password', 'required': 'required'}),
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserprofileForm(UserChangeForm):
    password = None
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'type': 'text'}),
    )
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
        required=False,
    )
    
    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:
            # Ensure the uploaded file is an image
            if not profile_pic.content_type.startswith('image'):
                raise forms.ValidationError('File is not an image')
            # Ensure the uploaded file size is within limits (adjust as needed)
            if profile_pic.size > 5 * 1024 * 1024:  # 5 MB
                raise forms.ValidationError('File size must be no more than 5 MB')
        return profile_pic
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = int(phone_number)
        if not (1000000000 <= phone_number <= 999999999999):  
            raise forms.ValidationError('Invalid phone number')
        return phone_number

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_pic']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        }

class AdminprofileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        # Apply custom styles and fonts to the fields
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].widget.attrs.update({'class': 'custom-input', 'placeholder': field_name.replace('_', ' ').capitalize(), 'style': 'font-family: "Open Sans", sans-serif;'})

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['fullname', 'address', 'email', 'phone_number', 'pincode']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': '2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pin-code'}),
        }