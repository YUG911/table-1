from django.db import models


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.role_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password_hash = models.CharField(max_length=255)
    address = models.CharField(max_length=500, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')
    is_verified = models.BooleanField(default=False)
    account_status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.full_name


class StateMaster(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'state_master'

    def __str__(self):
        return self.state_name


class CityMaster(models.Model):
    city_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE, db_column='state_id')
    city_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'city_master'

    def __str__(self):
        return self.city_name


class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    clinic_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.ForeignKey(CityMaster, on_delete=models.CASCADE, db_column='city_id')
    contact_number = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clinics'

    def __str__(self):
        return self.clinic_name


class DayMaster(models.Model):
    day_id = models.AutoField(primary_key=True)
    day_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'day_master'

    def __str__(self):
        return self.day_name


class ClinicHours(models.Model):
    hours_id = models.AutoField(primary_key=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')
    day = models.ForeignKey(DayMaster, on_delete=models.CASCADE, db_column='day_id')
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        db_table = 'clinic_hours'

    def __str__(self):
        return f"{self.clinic.clinic_name} - {self.day.day_name}"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'

    def __str__(self):
        return self.user.full_name


class ClinicStaff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')

    class Meta:
        db_table = 'clinic_staff'

    def __str__(self):
        return self.user.full_name


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    access_level = models.CharField(max_length=50)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return self.user.full_name


class VerificationLog(models.Model):
    verification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column='admin_id')
    status = models.CharField(max_length=20)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'verification_log'

    def __str__(self):
        return f"{self.user.full_name} - {self.status}"
