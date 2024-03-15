from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name',  'last_name', 'is_store_keeper', 'email', 'is_superuser', 'phone_number', 'department', 'doctor_type', 'doctor_specialization', 'is_chief_consultant', 'is_hod']
        
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
    
        # Add additional attributes or customize widgets if needed
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'first_name'  
        })
        
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'last_name'  
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'name': 'email'  
        })
    
        self.fields['is_superuser'].widget.attrs.update({
            'class': 'form-control',
            'name': 'is_superuser'  
        })
        
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'name': 'phone_number'  
        })
        
   
    
        # self.fields['is_chief_consultant'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'is_superuser'  
        # })
    
        self.fields['doctor_type'].widget.attrs.update({
            'class': 'form-control',
            'name': 'doctor_type'  
        })
    
        self.fields['doctor_specialization'].widget.attrs.update({
            'class': 'form-control',
            'name': 'doctor_specialization'  
        })
        
        excluded_departments = ['CEO']  # List of departments to exclude
        self.fields['department'].queryset = Department.objects.exclude(name__in=excluded_departments)
        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'name': 'department'  
        })



class DepartmentForm(forms.ModelForm):
     class Meta:
        model = Staff
        fields = '__all__'
        
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('registrar',)
        
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
    
        # Add additional attributes or customize widgets if needed
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'first_name'  
        })
        
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'last_name'  
        })
        
        
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'name': 'phone_number'  
        })
        
        self.fields['religion'].widget.attrs.update({
            'class': 'form-control',
            'name': 'religion'  
        })
        self.fields['ethnic_group'].widget.attrs.update({
            'class': 'form-control',
            'name': 'ethnic_group'  
        })
       
        
        self.fields['place_of_origin'].widget.attrs.update({
            'class': 'form-control',
            'name': 'place_of_origin'  
        })
        
        
        self.fields['dob'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'name': 'dob'  
        })
        
        self.fields['next_of_kin'].widget.attrs.update({
            'class': 'form-control',
            'name': 'next_of_kin'  
        })
        
        self.fields['address_of_kin'].widget.attrs.update({
            'class': 'form-control',
            'name': 'address_of_kin'  
        })
        
        self.fields['occupation'].widget.attrs.update({
            'class': 'form-control',
            'name': 'occupation'  
        })
        
        self.fields['marriage_status'].widget.attrs.update({
            'class': 'form-control',
            'name': 'marriage_status'  
        })
        
        self.fields['patient_type'].widget.attrs.update({
            'class': 'form-control',
            'name': 'patient_type'  
        })
        
        self.fields['next_of_kin_phone'].widget.attrs.update({
            'class': 'form-control',
            'name': 'next_of_kin_phone'  
        })
        
        self.fields['gender'].widget.attrs.update({
            'class': 'form-control',
            'name': 'gender'  
        })
        
        self.fields['card_number'].widget.attrs.update({
            'class': 'form-control',
            'name': 'card_number',  
            'readonly': ''
        })
        
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
    
        # Add additional attributes or customize widgets if needed
        self.fields['appointment_type'].widget.attrs.update({
            'class': 'form-control',
            'name': 'appointment_type'  
        })
        
        self.fields['doctor'].widget.attrs.update({
            'class': 'form-control',
            'name': 'doctor'  
        })   
        
    def clean(self):
        cleaned_data = super().clean()
        appointment_type = cleaned_data.get('appointment_type')
        doctor = cleaned_data.get('doctor')
        labprice = cleaned_data.get('labprice')

        # Check if either a doctor or a lab test is selected
        if appointment_type == 'Consultation' and not doctor:
            raise forms.ValidationError('Consultation appointment requires selection of a doctor')
        elif appointment_type == 'LabTest' and not labprice:
            raise forms.ValidationError('Lab Test appointment requires selection of a lab test')

        return cleaned_data    
        
        
class VitalForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        exclude = ['nurse', 'appointment']
        
    def __init__(self, *args, **kwargs):
        super(VitalForm, self).__init__(*args, **kwargs)
    
        # Add additional attributes or customize widgets if needed
        self.fields['weight'].widget.attrs.update({
            'class': 'form-control',
            'name': 'weight'  
        })
        self.fields['blood_pressure'].widget.attrs.update({
            'class': 'form-control',
            'name': 'blood_pressure'  
        })
        
        self.fields['pulse_rate'].widget.attrs.update({
            'class': 'form-control',
            'name': 'pulse_rate'  
        })    
        
        self.fields['temperature'].widget.attrs.update({
            'class': 'form-control',
            'name': 'temperature'  
        })    
        
        self.fields['note'].widget.attrs.update({
            'class': 'form-control',
            'name': 'note'  
        })    
     
     
     
class labPriceForm(forms.ModelForm):
    class Meta:
        model = labPrice
        fields = ['name', 'price']
        
    def __init__(self, *args, **kwargs):
        super(labPriceForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'name'  
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'name': 'price'  
        })


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['result' , 'test', 'file_name']
        
    def __init__(self, *args, **kwargs):
        super(LabResultForm, self).__init__(*args, **kwargs)
        self.fields['result'].widget.attrs.update({'class': 'form-control'})
        self.fields['test'].widget.attrs.update({'class': 'form-control'})
        self.fields['file_name'].widget.attrs.update({'class': 'form-control',  'accept': '.docx, .pdf'})



class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['name', 'patient']
        
    def __init__(self, *args, **kwargs):
        super(LabTestForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'name'  
        })

  
class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super(DrugForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'name'  
        })
     
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'name': 'price'  
        })
     
        self.fields['brand'].widget.attrs.update({
            'class': 'form-control',
            'name': 'brand'  
        })
     
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
            'name': 'quantity'  
        })
        
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['diagnosis', 'plan', 'complaint', 'examination']
        
        
    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        self.fields['complaint'].widget.attrs.update({
            'class': 'form-control',
            'name': 'complaint'  
        })
     
        self.fields['examination'].widget.attrs.update({
            'class': 'form-control',
            'name': 'examination'  
        })
     
        self.fields['diagnosis'].widget.attrs.update({
            'class': 'form-control',
            'name': 'diagnosis'  
        })
     
        self.fields['plan'].widget.attrs.update({
            'class': 'form-control',
            'name': 'plan'  
        })
     

  
class CardForm(forms.ModelForm):
    class Meta:
        model = CardPrice
        fields = ['card_type', 'price']
        
        
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)

        self.fields['card_type'].widget.attrs.update({
            'class': 'form-control',
            'name': 'card_type'  
        })
     
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'name': 'price'  
        })
     
     

class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control  showhide-password',
                                          'placeholder': 'Enter Your New Password',
                                          'name': 'new_passwprd'
                                         
                                          }),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control  showhide-password',
                                          'placeholder': 'Re-enter Your Password',
                                           'name': 'confirm_password',
                                          }),
    )
        
        
   
class ResetPasswordForm(forms.Form):
    username = forms.CharField(
        label="Staff Username",
        widget=forms.TextInput(attrs={'class': 'form-control ',
                                          'placeholder': 'Enter Staff Username',
                                          'name': 'username',
                                          'value': '',
                                          'autocomplete': 'off'
                                          }),
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control  showhide-password',
                                          'placeholder': 'Enter Your New Password',
                                          'name': 'new_password'
                                         
                                          }),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control  showhide-password',
                                          'placeholder': 'Re-enter  Password',
                                           'name': 'confirm_password',
                                          }),
    )
        
        
   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        