from django.contrib import admin
from .models import *



class DepartmentAdmin(admin.ModelAdmin) :
    list_display = ('name',)
    

class PatientAdmin(admin.ModelAdmin) :
    list_display = ('first_name', 'last_name', 'phone_number', 'dob', 'next_of_kin', 'address_of_kin', 'occupation', 'ethnic_group','place_of_origin', 'religion', 'patient_type', 'marriage_status', 'next_of_kin_phone', 'created_at', 'updated_at')


# class StaffUserAdmin(admin.ModelAdmin):
#     list_display = ('phone_number', 'email', 'first_name', 'last_name')


class StaffAdmin(admin.ModelAdmin):
    # Customize the Staff admin as needed
    pass
admin.site.register(Staff, StaffAdmin)








admin.site.register(Department, DepartmentAdmin)
admin.site.register(Patient, PatientAdmin)


# admin.site.register(MedicalRecord, MedicalRecordAdmin)
# admin.site.register(Billing, BillingAdmin)
# admin.site.register(Prescription, PrescriptionAdmin)
# admin.site.register(Drug, DrugAdmin)
# admin.site.register(LabTest, LabTestAdmin)
# admin.site.register(LabResult, LabResultAdmin)