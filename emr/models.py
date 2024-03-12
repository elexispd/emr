import random
import time
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from emr.utils import ethnic_groups



class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Staff(AbstractUser):
    phone_number = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey("Department",on_delete=models.CASCADE, null=True, default=None)
    doctor_type = models.CharField(max_length=100, null=True, blank=True)  # contract or permanent
    doctor_specialization = models.CharField(max_length=100, null=True, blank=True)
    is_chief_consultant = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_store_keeper = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    
    # Define related_name for groups and user_permissions
    # Make groups nullable
    groups = models.ManyToManyField(
        Group,
        related_name='staff_users',
        blank=True,  # Allow blank values
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='staff_users',
        help_text=_('Specific permissions for this user.'),
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only set the password if the user is being created (not updated)
            # Set the default password
            self.set_password('password1')  
        
        # Generate the username based on the count of existing Staff objects with "CBH" prefix
        if not self.username:
            prefix = "CBH"
            count = Staff.objects.filter(username__startswith=prefix).count() + 1
            self.username = f"{prefix}{count:03d}"  # Zero-padded 3-digit count
        
        super().save(*args, **kwargs)



class Patient(models.Model):
    MARRIAGE_STATUS = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widow', 'Widow(er)'),
    )
    PATIENT_TYPE = (
        ('in-patient', 'In-Patient'),
        ('out-patient', 'Out-Patient'),
        ('emergency', 'Emergency')
    )
    
    RELIGION = (
        ('christainity', 'Christianity'),
        ('islam', 'Islam'),
        ('tradional', 'Tradional'),
        ('judaism', 'Judaism'),
        ('other', 'Other'),
    )
    
    ETHIC_GROUP = ethnic_groups()
    
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    card_number = models.ForeignKey("Card",on_delete=models.CASCADE)
    next_of_kin = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    doctor = models.ForeignKey("Staff",on_delete=models.CASCADE, null=True, default=None)
    registrar = models.ForeignKey("Staff", related_name="registrar", on_delete=models.CASCADE, null=True, default=None)
    address_of_kin = models.CharField(max_length=200, null=True, blank=True)
    place_of_origin = models.CharField(max_length=100)
    marriage_status = models.CharField(max_length=50, choices=MARRIAGE_STATUS)
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPE)
    gender = models.CharField(max_length=50, choices=GENDER)
    next_of_kin_phone = models.BigIntegerField(null=True, blank=True)
    ethnic_group = models.CharField(max_length=100, choices=ETHIC_GROUP)
    occupation = models.CharField(max_length=100)
    religion = models.CharField(max_length=100, choices=RELIGION)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "
    


class Billing(models.Model):
    SERVICE_TYPES = (
        ('Consultation', 'Consultation'),
        ('LabTest', 'Lab Test'),
        ('XRay', 'X-Ray'),
        ('DrugSale', 'Drug Sale'),
        ('NewCard', 'New Card'),
        ('CardRenewal', 'Card Renewal')
    )
    METHOD = (
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
       
    )

    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    service_id = models.ForeignKey('Appointment', on_delete=models.CASCADE, null=True, blank=True)
    sold_drug = models.ForeignKey('SoldDrug', on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey('Card', on_delete=models.CASCADE, null=True, blank=True)
    is_card_renewal = models.BooleanField(default=False)
    invoice_id = models.BigIntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
   

class IncomeStream(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"


class IncomeRecord(models.Model):
    income_stream = models.ForeignKey(IncomeStream, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ref_code = models.BigIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.income_stream}"
    
class ApprovedIncomeRecord(models.Model):
    ref_code = models.ForeignKey(IncomeRecord, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)


class CardPrice(models.Model):
    TYPES = (
        ('new', 'New Card'),
        ('renew', 'Card Renewal'),
    )
    card_type = models.CharField(max_length=20, choices=TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)  # Set default value to True
    
    def __str__(self):
        return self.card_type
    


class Card(models.Model):
    card_number = models.BigIntegerField()
    is_expired = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return str(self.card_number)

   
class Appointment(models.Model):
    
    APPOINTMENT_TYPE_CHOICES = [
        ('Consultation', 'Consultation'),
        ('LabTest', 'Lab Test'),
        ('XRay', 'X-Ray'),
        
    ]
    
    
    patient = models.ForeignKey('Patient', related_name='appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Staff', on_delete=models.CASCADE, null=True, blank=True)
    labprice = models.ForeignKey('labPrice', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=1, default=0)
    appointment_date = models.DateTimeField(auto_now_add=True)
    appointment_type = models.CharField(max_length=100, choices=APPOINTMENT_TYPE_CHOICES)
    
    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if the object is being created for the first time
        super().save(*args, **kwargs)

        if is_new:
            Billing.objects.create(
                service_type=self.appointment_type,
                service_id=self,
                payment_status=False,
            )

            # Create LabTest record only if the appointment type is 'LabTest'
            if self.appointment_type == 'LabTest' and self.labprice:
                LabTest.objects.create(
                    patient=self.patient,
                    name=self.labprice,
                    appointment=self
                )

    def __str__(self):
        return f"{self.patient}"
    
    
class VitalSigns(models.Model):
    appointment = models.ForeignKey('Appointment', related_name='vitalsigns', on_delete=models.CASCADE)
    pulse_rate = models.FloatField(max_length=12)
    blood_pressure = models.FloatField(max_length=12, null=True,blank=True)
    temperature = models.FloatField(max_length=12, null=True,blank=True)
    weight = models.FloatField(max_length=12, default=0)
    nurse = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='nurse_vitalsigns')
    doctor = models.ForeignKey('Staff', on_delete=models.CASCADE, null=True, blank=True, related_name='doctor_vitalsigns')
    note = models.TextField(null=True,blank=True)
    
    

class labPrice(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
         return f"{self.name}"



class LabTest(models.Model):    
    patient = models.ForeignKey('Patient',  on_delete=models.CASCADE)
    name = models.ForeignKey('labPrice',  on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"



class LabResult(models.Model):
    test = models.ForeignKey('LabTest', on_delete=models.CASCADE)
    file_name = models.FileField(upload_to='static/labresults/', blank=True, null=True)
    result = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.result}" 
    




class Drug(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    

class SoldDrug(models.Model):
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default="pending")
    order_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    

class PrescribedDrug(models.Model):
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    drug = models.CharField(max_length=100, null=True, blank=True)
    dosage = models.CharField(max_length=100, null=True, blank=True)
    frequency = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)


class Prescription(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    complaint = models.TextField()
    examination = models.TextField()
    diagnosis = models.TextField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    