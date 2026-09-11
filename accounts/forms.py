from django import forms
from accounts.models import User, Role, Patient, Clinic, ClinicStaff, Admin, StateMaster, CityMaster
from doctors.models import Doctor, SpecializationMaster, QualificationMaster


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


class RegisterForm(forms.Form):
    ROLE_CHOICES = [
        (3, 'Clinic'),
        (1, 'Patient'),
        (2, 'Doctor'),
        (4, 'Clinic Staff'),
    ]

    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a strong password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'})
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already registered.")
        return phone


class PatientProfileForm(forms.Form):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                               widget=forms.RadioSelect)
    blood_group = forms.ChoiceField(choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    emergency_contact = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))


class DoctorProfileForm(forms.Form):
    doctor_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    new_patient_fee = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    old_patient_fee = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    about = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    specializations = forms.ModelMultipleChoiceField(
        queryset=SpecializationMaster.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    qualifications = forms.ModelMultipleChoiceField(
        queryset=QualificationMaster.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class ClinicForm(forms.Form):
    clinic_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.ModelChoiceField(queryset=StateMaster.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=CityMaster.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ClinicHoursForm(forms.Form):
    day_1_open = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    day_1_close = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    # ... etc for each day


class AdminForm(forms.Form):
    access_level = forms.ChoiceField(choices=[
        ('super', 'Super Admin'),
        ('manager', 'Manager')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
