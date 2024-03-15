import os
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages
from django.contrib.auth import logout as logouts, authenticate, login
from .forms import *
from .models import *
from django.urls import reverse
from django.db.models import Q, Sum
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime, timezone, timedelta
import uuid
from django.db import transaction
# import random, time, datetime
import random, time
from django.db import IntegrityError
from django.db.models import Count, Max
from .utils import *
from .decorators import department_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def home(request):
    return render(request, 'main.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form}) 


def logout(request):
    logouts(request)
    return redirect('login')





@login_required
def dashboard(request):

    staff_queryset = Staff.objects.all()
    patients_queryset = Patient.objects.values('first_name', 'last_name', 'phone_number', 'address_of_kin')

    # Convert queryset to list to use random.sample()
    staff_list = list(staff_queryset)
    patients_list = list(patients_queryset)
    

    doctor_total = staff_queryset.filter(department__name='Doctor').count()
    nurse_total = staff_queryset.filter(department__name='Nursing').count()
    pharmacist_total = staff_queryset.filter(department__name='Pharmacy').count()
    record_total = staff_queryset.filter(department__name='Records').count()
    

    # Randomly select 10 staff and patients
    random_staff = random.sample(staff_list, min(len(staff_list), 10))
    random_patients = random.sample(patients_list, min(len(patients_list), 10))

    context = {
        'staff': random_staff,
        'patients': random_patients,
        'doctor_total': doctor_total,
        'nurse_total': nurse_total,
        'record_total': record_total,
        'pharmacist_total': pharmacist_total
    }
    return render(request, 'dashboard.html', context)



@login_required

def search_patient(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        card_number = request.POST.get('card_number')
        all_patients = request.POST.get('all')
        range = request.POST.get('date_range')
        

        patients_list = Patient.objects.all()

        if keyword:
            patients_list = patients_list.filter(
                models.Q(first_name__icontains=keyword) |
                models.Q(last_name__icontains=keyword) |
                models.Q(phone_number=keyword) 
            )
            context = {'patients': patients_list}
            return render(request, 'patients.html', context)
        elif card_number:
            try:
                card = Card.objects.get(card_number=card_number)
                patient = Patient.objects.get(card_number=card.id)
                return redirect(reverse('get_patient', kwargs={'user_id': patient.id}))
            except:
                messages.info(request, "No Patient Found", extra_tags="info")
            
        elif range:
 
            try:
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
  
                patients_list = patients_list.filter(
                    models.Q(created_at__range=[from_date, to_date])
                )
                context = {'patients': patients_list}
                return render(request, 'patients.html', context)
            except:
                messages.info(request, "No Patient Found", extra_tags="info")
            
            
           
                
        elif all_patients == 'all':
            context = {'patients': patients_list}
            return render(request, 'patients.html', context)

    # Render the search page for both GET requests and failed POST requests
    return render(request, 'search_patient.html')

      
@login_required
def view_staff(request, id):
    staff = Staff.objects.get(id=id)
    context = {'staff' : staff}
    return render(request, 'staff/staff-details.html', context)  


@login_required
def get_patients(request):
    pateints = Patient.objects.all()
    context = {'patients' : pateints}
    return render(request, 'patients.html', context)
 

@login_required
def get_patient(request, user_id):
    pateint = Patient.objects.get(id=user_id)
    context = {'patient' : pateint}
    return render(request, 'patient-details.html', context)
 
 
@login_required
def update_patient(request, user_id):
    patient = Patient.objects.get(id=user_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)  # Pass instance to the form
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient Successfully Updated')
            return redirect(reverse('update_patient', kwargs={'user_id': patient.id}))
    else:
        form = PatientForm(instance=patient)  # Pass instance to the form

    doctors = Staff.objects.filter(department__name__icontains='doctor')
    context = {'form': form, 'doctors': doctors, 'patient': patient}
    return render(request, 'edit_patient.html', context)
 
 
 
@login_required
def add_patient(request):
    if request.method == "POST": 
        card_number = request.POST.get('card_number')
        if 'search' in request.POST: 
            if Card.objects.filter(card_number=card_number).exists():
                card = Card.objects.get(card_number=card_number)
                form = PatientForm()
            else:
                messages.error(request, f'{card_number} Is Not A Valid Card Number', extra_tags='danger')
                return redirect('register_search_card')
            
            
        elif 'search' not in request.POST : # this post should be for registraion and not for the POST that comes from register_search_card
            card = Card.objects.get(id=card_number)
            form = PatientForm(request.POST)
            form.instance.card_number = card
            form.instance.registrar = request.user

            if form.is_valid() :
                form.save()
                messages.success(request, 'Patient Successfully Registered')
                return redirect('register_patient')
        else:
            return redirect('register_search_card')
        doctors = Staff.objects.filter(department__name__icontains = 'doctor')
        context = {'form':form, 'doctors': doctors, 'card': card}
        return render(request, 'add_patient.html', context)
    else:
        return redirect('register_search_card')
 
 
def register_search_card(request):
    return render(request, 'register-patient-card-search.html')
 
 
 
@login_required
@department_required(['Admin', 'Ceo'])
def search_staff(request):
    print(request.user.department.name)
    excluded_departments = ['CEO']
    departments = Department.objects.exclude(name__in=excluded_departments)
    if request.POST:
        keyword = request.POST.get('keyword')
        department_id = request.POST.get('department')
        all_staff = request.POST.get('all')

        staff_list = Staff.objects.exclude(username__in=excluded_departments)

        if keyword:
            staff_list = staff_list.filter(
                models.Q(first_name__icontains=keyword) |
                models.Q(last_name__icontains=keyword)
            )
        elif department_id:
            staff_list = staff_list.filter(department_id=department_id)
        elif all_staff == 'all':
            all_staff = all_staff

        context = {'staff_list': staff_list}
        return render(request, 'staff/search_staff_results.html', context)
    else:
        # Render search form page
        return render(request, 'staff/search_staff.html', {'departments': departments})
        

 
@login_required
@department_required(['Admin', 'Ceo'])
def add_staff(request):
    form = StaffForm()
    if request.method == 'POST' :
        form = StaffForm(request.POST)
        
        if form.is_valid() :
            form.save()
            messages.success(request, 'Staff Successfully Registered')
            return redirect('add_staff')

    context = {'form':form}
    return render(request, 'staff/add_staff.html', context)
 
 
@login_required
@department_required(['Doctor', 'Nursing'])
def add_vital(request, appointment_id):
    try:
        vital_signs = VitalSigns.objects.get(appointment_id=appointment_id)
    except ObjectDoesNotExist:
        vital_signs = None

    form = VitalForm(instance=vital_signs)
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        form = VitalForm(request.POST, instance=vital_signs)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.appointment = appointment
            vital.nurse = request.user
            vital.save()
            messages.success(request, 'Vital was taken successfully')
            return redirect(reverse('add_vital', kwargs={'appointment_id': appointment.id}))
    context = {'form': form, 'has_vitalsigns': vital_signs is not None}
    return render(request, 'nursing/add_vital.html', context)



 
 
@login_required
@department_required(['Records', 'Doctor', 'Nursing'])
def appointments(request):
    today = date.today()
    appointments = Appointment.objects.filter(appointment_type="Consultation",appointment_date__date=today)
    context = {'appointments': appointments}
    return render(request, 'appointment/patient_appointments.html', context)
 
@login_required
@department_required(['Records', 'Doctor'])
def scheduled_appointments(request): 
    current_date = date.today()
    user = request.GET.get('q')
    if user:
        appointments = Appointment.objects.filter(patient_id=user, appointment_date__gt=current_date)
    else:
        appointments = Appointment.objects.filter(appointment_date__gt=current_date)
    context = {'scheduled_appointments': appointments}
    return render(request, 'appointment/scheduled.html', context)
 
 
@login_required
@department_required(['Records'])
def book_appointment(request, user_id):
    patient = Patient.objects.get(id=user_id)
    tests = labPrice.objects.all()
    form = AppointmentForm()
  
    if request.method == 'POST' :
        form = AppointmentForm(request.POST)
        
        if form.is_valid() :
            form.save()
            messages.success(request, 'Appointment Booked Successfully')
            return redirect(reverse('book_appointment', kwargs={'user_id': user_id}))
    
    consultants = Staff.objects.exclude(
        Q(department__name__iexact='admin') |
        Q(department__name__iexact='billing') |
        Q(department__name__iexact='pharmacy') |
        Q(department__name__iexact='nursing') |
        Q(department__name__iexact='lab') |
        Q(department__name__iexact='records') 
    )
    context = {'form':form, 'consultants': consultants, 'patient': patient, 'tests': tests}
    return render(request, 'appointment/book.html', context)

@department_required(['Doctor'])
def book_appointment_doctor(request, user_id, appointment_id):
     if request.method == 'POST' :    
        try:
            patient = Patient.objects.get(id=user_id)
            appointment_date = request.POST.get('date')
           
            appointment = Appointment.objects.create(
                patient_id=user_id,
                appointment_date=appointment_date,
                doctor_id=request.user.id,
                appointment_type='Consultation' 
            )
            messages.success(request, f'Next Appointment Scheduled on {appointment_date}')
            return redirect('add_prescription', user_id=user_id, appointment_id=appointment_id)
        except ObjectDoesNotExist:
            messages.error(request, f'Patient not found.{patient}', extra_tags='danger')
            return redirect('add_prescription', user_id=user_id, appointment_id=appointment_id)

         
 
@login_required
@department_required(['Billing'])
def consultation_payments(request, status):
    if status == 'paid':
        # Retrieve paid consultation payments
        payments = Billing.objects.filter(service_type='Consultation', payment_status=True)
        context = {
            'payments': payments,
            'status': 'Paid'
        }
        return render(request, 'payments/payments.html', context)
    elif status == 'unpaid':
        payments = Billing.objects.filter(service_type='Consultation', payment_status=False)
        context = {'payments': payments}
        return render(request, 'payments/payments.html', context)
    
    elif status == 'all':
        payments = Billing.objects.filter(service_type='Consultation')
        context = {
            'payments': payments,
            'status': 'all'
        }
        return render(request, 'payments/payments.html', context)
    else:
        pass


@login_required
@department_required(['Billing'])
def lab_payments(request, status):
    if status == 'paid':
        # Retrieve paid consultation payments
        payments = Billing.objects.filter(service_type='LabTest', payment_status=True)
        context = {
            'payments': payments,
            'status': 'Paid'
        }
        return render(request, 'payments/lab_payments.html', context)
    elif status == 'unpaid':
        payments = Billing.objects.filter(service_type='LabTest', payment_status=False)
        context = {'payments': payments}
        return render(request, 'payments/lab_payments.html', context)
    
    elif status == 'all':
        payments = Billing.objects.filter(service_type='LabTest')
        context = {
            'payments': payments,
            'status': 'all'
        }
        return render(request, 'payments/lab_payments.html', context)
    else:
        # Handle invalid status
        pass



 
@login_required
@department_required(['Billing'])
def payments(request):
     return render(request, 'payment-list.html')
 

@login_required
@department_required(['Billing'])
def confirm_payment(request):
    return render(request, 'confirm-payment.html')

@login_required
@department_required(['Billing'])
def confirm_appointment_payment(request, billing_id):
    billing = Billing.objects.get(id=billing_id)
    
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        if not total_amount:
            messages.error(request, 'Total amount is required.', extra_tags='danger')
            context = {'bill': billing,}
            return render(request, 'payments/confirm-appointment.html', context)
        
        try:
            total_amount = float(total_amount)
        except ValueError:
            messages.error(request, 'Total amount must be a valid number.', extra_tags='danger')
            context = {'bill': billing}
            return render(request, 'payments/confirm-appointment.html', context)
        
        appointment = Appointment.objects.get(id=billing.service_id.id)
       # Update appointment & billing object and generate invoice ID within a transaction
        with transaction.atomic():
            billing.total_amount = total_amount
            billing.payment_status = True
            billing.payment_date= date.today()
            billing.invoice_id = generate_invoice_id()  # Define your generate_invoice_id function
            appointment.status = 1
            appointment.save()
            billing.save()
        
        return redirect(reverse('invoice', kwargs={'qid': billing_id}))


    context = {'bill': billing}
    return render(request, 'payments/confirm-appointment.html', context)


@login_required
@department_required(['Billing'])
def confirm_drug_payment(request, order_id):
    sold_drugs = SoldDrug.objects.filter(order_id=order_id)
    total_price = sum(sold_drug.quantity * sold_drug.price for sold_drug in sold_drugs)
    status = sold_drugs.first().status
    billing = Billing.objects.get(sold_drug__order_id=order_id)
    if request.method == "POST":
        with transaction.atomic():
            # Update billing details
            billing.total_amount = total_price
            billing.payment_status = True
            billing.payment_date = date.today()
            billing.invoice_id = generate_invoice_id()
            billing.save()
            
            # Update status for all sold drugs
            for sold_drug in sold_drugs:
                sold_drug.status = "paid"
                sold_drug.save()
        return redirect(reverse('invoice', kwargs={'qid': billing.id}))

    context = {'sold_drugs': sold_drugs, 'order_id': order_id, 'total_price': total_price, 'status': status, 'billing_id': billing.id}
    return render(request, 'payments/confirm-drug.html', context)

 
@login_required
@department_required(['Billing'])
def invoice(request, qid):
    try:
        billing = Billing.objects.get(id=qid)
        if billing.service_type == 'DrugSale':
            sold_drugs = SoldDrug.objects.filter(order_id=billing.sold_drug.order_id)
            context = {'bill': billing, 'sold_drugs': sold_drugs}
            return render(request, 'payments/invoice.html', context)
        else:
            context = {'bill': billing}
            return render(request, 'payments/invoice.html', context)
    except Billing.DoesNotExist:
        return render(request, '404.html')

 

@login_required
@department_required(['Lab'])
def add_lab_test(request, user_id):
    form = LabTestForm()
    patient = Patient.objects.get(id=user_id)
    if request.method == "POST":
        form = LabTestForm(request.POST)
        if form.is_valid() :
            test = form.save(commit=False)
            test.patient_id = patient.id
            test.save()
            messages.success(request, 'Test Added Successfully')
            return redirect(reverse('add_lab_test', kwargs={'user_id': user_id}))
    context = {'form': form, 'patient': patient}
    return render(request, 'lab/add_lab_test.html', context)
 
 
@login_required
@department_required(['Doctor', 'Lab'])
def lab_list(request):
    tests = LabTest.objects.all().order_by('-created_at')
    context = {'tests': tests}
    return render(request, 'lab/lab-list.html', context)

@login_required
@department_required(['Lab', 'Doctor'])
def patient_lab_tests(request,user_id):
    tests = LabTest.objects.filter(patient_id=user_id).order_by('-created_at')
    patient = Patient.objects.get(id=user_id)
    context = {'tests': tests, 'name': patient}
    return render(request, 'lab/patient-lab-list.html', context)
 


@login_required
@department_required(['Lab'])
def add_lab_result(request, id):
    try:
        test = LabTest.objects.get(id=id)
        form = LabResultForm(request.POST or None, request.FILES or None)
        
        exist = LabResult.objects.filter(test_id=id).exists()
        
        if request.method == 'POST':
            if form.is_valid():
                lab_result = form.save(commit=False)
                lab_result.lab_test_id = test.id
                if 'file' in request.FILES:
                    uploaded_file = request.FILES['file']
                    upload = file_upload(uploaded_file, '/static/labresults')
                    
                    if upload == 0:
                        messages.error(request, 'Only PDF and Docx are acceptable', extra_tags="danger")
                        return redirect(reverse('add_lab_result', kwargs={'id': id}))
                    else:
                        uploaded_file = request.FILES['file']
                        lab_result.file_name = upload
                elif 'result' in form.cleaned_data and form.cleaned_data['result']:
                    lab_result.result = form.cleaned_data['result']
                lab_result.save()

                messages.success(request, 'Result Uploaded Successfully')
                return redirect(reverse('add_lab_result', kwargs={'id': id}))
        context = {'form': form, 'test':test, 'exist': exist}
        return render(request, 'lab/add_lab_result.html', context)
    except LabTest.DoesNotExist:
        return render(request, '404.html') 
 
 
@department_required(['Lab', 'Doctor'])
def view_lab_result(request, test_id):
    try:   
        test = LabResult.objects.get(test_id=test_id)
        context = {'result': test}
        return render(request, 'lab/view_result.html',context)
    except LabTest.DoesNotExist:
        return render(request, '404.html')


@login_required 
def lab_results(request):
    return render(request, 'lab/lab-result-list.html')
 

@login_required 
@department_required(['Lab'])
def add_lab_price(request):
    form = labPriceForm()
    if request.method == 'POST':   
        form = labPriceForm(request.POST)       
        if form.is_valid():
            form.save()
            messages.success(request, 'Test Price added Successfully')
            return redirect('add_lab_price')
        else:
            messages.error(request, 'Not valid', extra_tags="danger")
            
    context = {'form': form}

    return render(request, 'lab/add_lab_price.html',context)
   

@login_required 
@department_required(['Lab', 'Nursing', 'Doctor', 'Records', 'Admin'])
def lab_prices(request):
    tests = labPrice.objects.all()
    context = {'tests': tests}
    return render(request, 'lab/lab-prices.html', context)
 
 
@login_required
@department_required(['Pharmacy', 'Doctor'])
def prescriptions(request, user_id):
    patient_prescriptions = Prescription.objects.filter(appointment__patient_id=user_id)
    name = Patient.objects.get(id=user_id)
    context = {'patient_prescriptions': patient_prescriptions, 'name': name}
    return render(request, 'doctor/prescription_patient.html', context )
 
@login_required
@department_required(['Doctor', 'Pharmacy'])
def prescription(request, user_id, prescription_id):
    return render(request, 'doctor/prescription_detail.html')
 
 


@login_required
@department_required(['Doctor', 'Pharmacy'])
def prescribe_drug(request):
    # Grouping all results by prescription_id and annotating with the count
    prescribed_drugs = (
        PrescribedDrug.objects.values('prescription_id')
                               .annotate(total_drugs=Count('id'))
    )
    context = {'prescribed_drugs': prescribed_drugs}
    return render(request, 'drugs/prescribed-drugs.html', context)
 
 
@login_required
@department_required(['Doctor', 'Pharmacy']) 
def view_prescribed_drug(request, prescription_id):
    prescribed_drugs = PrescribedDrug.objects.filter(prescription_id=prescription_id)
    context = {'prescribed_drugs': prescribed_drugs}
    return render(request, 'drugs/view-prescribed-drugs.html', context)
 

@login_required
@department_required(['Doctor'])
def add_prescription(request, user_id, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    # Check if a prescription already exists for the appointment
    if Prescription.objects.filter(appointment=appointment).exists():
        
        has_prescription = 1
        prescription = Prescription.objects.get(appointment_id=appointment.id)
        drugs = PrescribedDrug.objects.filter(prescription_id=prescription.id)
        form = PrescriptionForm(instance=prescription)
        if drugs:
            pass
        else:
            drugs = PrescribedDrug.objects.none()

    else:
        has_prescription = 0 
        drugs = PrescribedDrug.objects.none()
        if request.method == 'POST':
            form = PrescriptionForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        prescription = Prescription.objects.create(
                            appointment=appointment,
                            complaint=form.cleaned_data['complaint'],
                            examination=form.cleaned_data['examination'],
                            diagnosis=form.cleaned_data['diagnosis'],
                            plan=form.cleaned_data['plan']
                        )
                        drugs = request.POST.getlist('drug[]')
                        dosages = request.POST.getlist('dosage[]')
                        frequencies = request.POST.getlist('frequency[]')
                        durations = request.POST.getlist('duration[]')
                        
                        appointment.status = "2"
                        appointment.save()
                        
            
                        if drugs and any(drugs):
                            dosages = request.POST.getlist('dosage[]')
                            frequencies = request.POST.getlist('frequency[]')
                            durations = request.POST.getlist('duration[]')
                            for i in range(len(drugs)):
                                if drugs[i]:  # Check if the drug name is not an empty string
                                    PrescribedDrug.objects.create(
                                        prescription=prescription,
                                        drug=drugs[i],
                                        dosage=dosages[i],
                                        frequency=frequencies[i],
                                        duration=durations[i]
                                    )
                    messages.success(request, 'Prescription Added Successfuly')
                    return redirect('add_prescription', user_id=user_id, appointment_id=appointment_id)

                except Exception as e:
                    pass
            else:
                pass
        else:
            form = PrescriptionForm()
        
    context = {'appointment': appointment, 'form': form, 'drugs': drugs, 'has_prescription': has_prescription }
    return render(request, 'doctor/prescription_add.html', context)
 
 
@login_required
@department_required(['Doctor', 'Pharmacy'])
def drug_list(request):
    drugs = Drug.objects.all()
    context = {'drugs' : drugs}
    return render(request, 'drugs/drugs.html', context)
 

@login_required
@department_required(['Pharmacy'])
def add_drug(request):
    form = DrugForm()
    if request.method == "POST":
        form = DrugForm(request.POST)       
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug added Successfully')
            return redirect('add_drug')
    context = {'form': form}
    return render(request, 'drugs/add-drug.html', context)


@login_required
@department_required(['Pharmacy'])
def update_drug(request, d_id):
    try:
        drug = Drug.objects.get(id=d_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    
    form = DrugForm(instance=drug) 
    if request.method == "POST":
        form = DrugForm(request.POST, instance=drug)      
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug Updated Successfully')
            return redirect('update_drug', d_id)
    context = {'form': form, 'edit': d_id}
    return render(request, 'drugs/add-drug.html', context)



@login_required
@department_required(['Pharmacy'])
def get_drug_details(request):
    if request.method == 'GET':
        drug_id = request.GET.get('drug_id')
        try:
            drug = Drug.objects.get(id=drug_id)
            data = {
                'price': drug.price,
                'available_quantity': drug.quantity
            }
            return JsonResponse(data)
        except Drug.DoesNotExist:
            return JsonResponse({'error': 'Drug not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
@department_required(['Pharmacy']) 
def sale_drug(request):
    drugs = Drug.objects.all()
    context = {'drugs': drugs}
    
    if request.method == "POST":
        names = request.POST.getlist('name[]')
        quantities = request.POST.getlist('quantity[]')
        
        # Ensure both name[] and quantity[] arrays have the same length
        if len(names) != len(quantities):
            messages.error(request, 'Invalid request data.', extra_tags='danger')
            return redirect('sale_drug')
        
        try:
            with transaction.atomic():
                order_id = generate_invoice_id()
                all_drugs_sold = True  # Flag to track if all drugs are sold successfully
                for name, quantity in zip(names, quantities):
                    drug = Drug.objects.get(id=name)
                    quantity_sold = int(quantity)
                    
                    # Check if quantity_sold is valid
                    if quantity_sold <= 0:
                        messages.error(request, 'Quantity must be a positive number.', extra_tags='danger')
                        return redirect('sale_drug')
                    
                    # Don't update quantity here
                    total_amount = drug.price * quantity_sold
                    sold_drug = SoldDrug.objects.create(
                        drug=drug,
                        price=drug.price,
                        quantity=quantity_sold,
                        order_id=order_id,
                        total_price=total_amount
                    )
                
                # Create a billing record for the drug sale if all drugs are sold successfully
                if all_drugs_sold:
                    Billing.objects.create(
                        service_type='DrugSale',
                        sold_drug=sold_drug,
                        total_amount=total_amount,
                        payment_status=False,  # Payment status initially set to False
                        payment_date=None  # Payment date initially set to None
                    )
                    messages.success(request, 'All drugs sold successfully')
                else:
                    messages.error(request, 'One or more drugs could not be sold due to insufficient quantity', extra_tags='danger')
        
        except Drug.DoesNotExist:
            messages.error(request, 'One or more drugs do not exist', extra_tags='danger')
    
    return render(request, 'drugs/sale-drug.html', context)

 
@login_required
@department_required(['Pharmacy']) 
def drugs_history(request):
    sold_drugs = SoldDrug.objects.values('order_id', 'drug__name', 'status').annotate(total_sold=Count('id'), latest_created_at=Max('created_at'))

    # Order the queryset in descending order by latest created_at
    sold_drugs = sold_drugs.order_by('-latest_created_at')
    context = {'sold_drugs': sold_drugs}
    return render(request, 'drugs/history.html', context)
 
 

@login_required
@department_required(['Pharmacy']) 
def drug_sell(request):
    sold_drugs = SoldDrug.objects.filter(status='Pending').values('order_id', 'drug__name', 'status').annotate(total_sold=Count('id'))
    context = {'sold_drugs': sold_drugs}
    return render(request, 'drugs/pending-drugs.html', context)


@login_required
@department_required(['Pharmacy'])
def drug_history_detail(request, order):
    sold_drugs = SoldDrug.objects.filter(order_id=order)
    status = sold_drugs.first().status
    
    # Check if all drugs are sold
    all_drugs_sold = all(sold_drug.status == 'paid' for sold_drug in sold_drugs)
    
    # If all drugs are sold, update the quantity
    if request.method == "POST":
        if all_drugs_sold:
            with transaction.atomic():
                for sold_drug in sold_drugs:
                    drug = sold_drug.drug
                    quantity_sold = sold_drug.quantity
                    drug.quantity -= quantity_sold
                    drug.save()
                    sold_drug.status = "dispensed"
                    sold_drug.save()
            # Redirect to the same page after updating the status
            return HttpResponseRedirect(request.path_info)
    
    context = {'sold_drugs': sold_drugs, 'status': status}
    return render(request, 'drugs/history-detail.html', context)
 
 

@department_required(['Billing']) 
def drug_payments(request, status):
    if status == 'paid':
        # Retrieve paid consultation payments
        payments = Billing.objects.filter(service_type='DrugSale', payment_status=True)
        context = {
            'payments': payments,
            'status': 'Paid'
        }
        return render(request, 'drugs/drug_payments.html', context)
    elif status == 'unpaid':
        payments = Billing.objects.filter(service_type='DrugSale', payment_status=False).order_by('-id')
        context = {'payments': payments}
        return render(request, 'drugs/drug_payments.html', context)
    
    elif status == 'all':
        payments = Billing.objects.filter(service_type='DrugSale')
        context = {
            'payments': payments,
            'status': 'all'
        }
        return render(request, 'drugs/drug_payments.html', context)
    else:
        # Handle invalid status
        pass
 
 
def validate_payment_type(payment_type_id):
    try:
        return int(payment_type_id)
    except ValueError:
        return None


def create_new_card_and_billing(payment_type, payment_method, cardprice):
    with transaction.atomic():
        expiration_date = date.today() + timedelta(days=60)
        card = Card.objects.create(card_number=generate_card_number(), expiration_date=expiration_date)
        billing = Billing.objects.create(
            service_type=payment_type,
            total_amount=cardprice.price,
            payment_method=payment_method,
            payment_status=True,
            invoice_id=generate_invoice_id(),
            payment_date=date.today(),
            card=card
        )
        billing.save()
        return card


def renew_card_and_create_billing(payment_type,payment_method, cardprice, card_number):
    try:
        expiration_date = date.today() + timedelta(days=60)
        card = Card.objects.get(card_number=card_number)
        card.expiration_date = expiration_date
        with transaction.atomic():
            card.save()
            billing = Billing.objects.create(
                service_type=payment_type,
                total_amount=cardprice.price,
                payment_method=payment_method,
                payment_status=True,
                is_card_renewal=True,
                invoice_id=generate_invoice_id(),
                payment_date=date.today(),
                card=card
            )
            billing.save()
            return card
    except Card.DoesNotExist:
        return None
    
    

@login_required
@department_required(['Billing']) 
def card_registration_payment(request):
    payment_types = CardPrice.objects.all()
    context = {"payment_types": payment_types}
    
    if request.method == "POST":
        payment_type_id = request.POST.get('payment_type')
        payment_method = request.POST.get('payment_method')
        
        
        if not payment_type_id:
            messages.error(request, 'Payment Type Is Required.', extra_tags='danger')
            return render(request, 'payments/card/new-card.html', context)
        
        payment_type_id = validate_payment_type(payment_type_id)
        if payment_type_id is None:
            messages.error(request, 'Invalid Activity Dictated', extra_tags='danger')
            return render(request, 'payments/card/new-card.html', context)
        
        try:
            cardprice = CardPrice.objects.get(id=payment_type_id)
            if cardprice.card_type == 'new':
                payment_type = "NewCard"
                card = create_new_card_and_billing(payment_type, payment_method, cardprice)
            elif cardprice.card_type == 'renew':
                payment_type = "CardRenewal"
                card_number = request.POST.get('card_number')
                card = renew_card_and_create_billing(payment_type, payment_method, cardprice, card_number)
                if card is None:
                    messages.error(request, 'Invalid Card Number.', extra_tags='danger')
                    return render(request, 'payments/card/new-card.html', context)
            else:
                messages.error(request, 'Invalid Card Payment Type.', extra_tags='danger')
                return render(request, 'payments/card/new-card.html', context)

            messages.success(request, f'Payment Successful: Card Number {card.card_number}')
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid Entry.', extra_tags='danger')

    return render(request, 'payments/card/new-card.html', context)
 
 
def get_card_price_details(request):
    if request.method == 'GET':
        price_id = request.GET.get('price_id')
        try:
            fee = CardPrice.objects.get(id=price_id)
            data = {
                'price': fee.price
            }
            return JsonResponse(data)
        except Drug.DoesNotExist:
            return JsonResponse({'error': 'Drug not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
        

@login_required
@department_required(['Billing', 'Admin']) 
def add_card_price(request):
    
    if request.method == 'POST':
        form = CardForm(request.POST) 
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Card Price Was Added')
            return redirect('add_card_price')
    else :
        form = CardForm()
    context = {'form': form}
    return render(request, 'payments/card/add-price.html', context)
 
 
@login_required
@department_required(['Billing']) 
def card_renewal_payment(request):
    return render(request, 'payments/card/card-renewal.html')


@login_required
@department_required(['Billing']) 
def card_payment_search(request):
    payment_types = CardPrice.objects.all()
    if request.method == "POST":
        # Check which form was submitted
        if 'payment_type' in request.POST:
            # Search by Payment Type
            payment_type_id = request.POST.get('payment_type')
            if payment_type_id:
                card_payments = Billing.objects.filter(service_type=payment_type_id)
            else:
                card_payments = Billing.objects.all()
        
        elif 'card_number' in request.POST:
            # Search by Card Number
            card_number = request.POST.get('card_number')
            if card_number:
                card_payments = Billing.objects.filter(card__card_number=card_number)
            else:
                card_payments = Billing.objects.all()
        
        elif 'date' in request.POST:
            # Search by Date
            date = request.POST.get('date')
            if date:
                card_payments = Billing.objects.filter(payment_date=date)
            else:
                card_payments = Billing.objects.all()
        
        elif 'all' in request.POST:
            # Search All Payments
            card_payments = Billing.objects.filter(service_type__in=['NewCard', 'CardRenewal'])
        
        context = {"payment_types": payment_types, "card_payments": card_payments}
        return render(request, 'payments/card/search_results.html', context)
        
    context = {"payment_types": payment_types }
    return render(request, 'payments/card/search.html', context)



@login_required
@department_required(['Admin']) 
def create_income_stream(request):    
    if request.method == 'POST':
        stream = request.POST.get('stream')
        if not stream:
            messages.error(request, "Field cannot be empty", extra_tags='danger')
            return redirect(create_income_stream)

        if IncomeStream.objects.filter(name__iexact=stream).exists():
            messages.error(request, f"Income stream '{stream}' already exists", extra_tags='danger')
            return redirect('create_income_stream')
        
        IncomeStream.objects.create(name=stream)
        messages.success(request, f"Income stream '{stream}' created successfully")
    return render(request, 'payments/account/create-stream.html')


@login_required
@department_required(['Billing', 'Admin']) 
def income_streams(request):    
    streams = IncomeStream.objects.all()
    context = {'streams': streams}
    return render(request, 'payments/account/income-streams.html', context)


@login_required
@department_required(['Billing']) 
def record_income_stream(request):    
    if request.method == 'POST':
        ref_code = generate_unique_numbers()
        for stream in IncomeStream.objects.all():
            amount = request.POST.get(str(stream.id))
            if amount is not None:  # Check if amount is not None or empty string
                if amount == '':
                    amount = 0
                IncomeRecord.objects.create(income_stream=stream, amount=amount, ref_code=ref_code)
                
        messages.success(request, f'Record Added Successfully')       
        return redirect('record_income_stream') 
    else:
        streams = IncomeStream.objects.all()
        context = {'streams': streams}
        return render(request, 'payments/account/record-stream-income.html', context )


@login_required
@department_required(['Billing', 'Admin', 'Account']) 
def view_income_stream(request):
    if request.method == "POST":
        if 'today' in request.POST:
            today = date.today()
            formatted_date = today.strftime("%dth %B, %Y")
            records = IncomeRecord.objects.filter(created_at=today)
            if records.exists():  # Check if records exist
                context = {'records': records, "caption": "Today"}
                return render(request, 'payments/account/show-account-record.html', context)
            else:
                messages.info(request, 'No record was found', extra_tags='info')
                return redirect('view_income_stream')
        elif 'date_range' in request.POST:
            try:
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

                # Format the dates
                formatted_from_date = from_date_obj.strftime("%dth %B, %Y")
                formatted_to_date = to_date_obj.strftime("%dth %B, %Y")
                records = IncomeRecord.objects.filter(created_at__range=[from_date, to_date]).values('ref_code', 'created_at').annotate(total=Count('ref_code'))
                if records.exists():  # Check if records exist
                    context = {'records': records, "caption": f"{formatted_from_date} - {formatted_to_date}"}
                    return render(request, 'payments/account/record-list.html', context)
                else:
                    messages.info(request, 'No record was found', extra_tags='info')
                    return redirect('view_income_stream')
            except ValueError:           
                messages.info(request, 'No record was found', extra_tags='info')
                return redirect('view_income_stream')
        elif 'all' in request.POST:
            try:
        
               
                records = IncomeRecord.objects.values('ref_code', 'created_at').annotate(total=Count('ref_code'))
                if records.exists():  # Check if records exist
                    context = {'records': records, "caption": f"All"}
                    return render(request, 'payments/account/record-list.html', context)
                else:
                    messages.info(request, 'No record was found', extra_tags='info')
                    return redirect('view_income_stream')
            except ValueError:           
                messages.info(request, 'No record was found', extra_tags='info')
                return redirect('view_income_stream')
        
    return render(request, 'payments/account/search.html')


@login_required
# @department_required(['Billing', 'Admin', 'Account']) 
def  view_income_stream_from_range(request):
            
    
    try:
        # ref_code = request.GET.get('ref_code')
        encrypted_ref_code = request.GET.get('ref_code')

        ref_code = decrypt_data(encrypted_ref_code)
        records = IncomeRecord.objects.filter(ref_code=ref_code)
         # Check if any of the records have an associated approved income record
        is_approved = any(ApprovedIncomeRecord.objects.filter(ref_code=record).exists() for record in records)
        context = {'records': records, 'is_approved':is_approved}
        
        if request.method == "POST":
            try:
                for record in records:
                    amount = request.POST.get(str(record.id))
                    if amount is not None:  # Check if amount is not None or empty string
                        if amount == '':
                            amount = 0
                        record.amount = amount
                        record.save()
                messages.success(request, f'Record updated Successfully')       
                return redirect(reverse('view_income_stream_from_range') + f'?ref_code={encrypted_ref_code}')
            except ObjectDoesNotExist:
                messages.error(request, f'Record was not updated', extra_tags="danger")       
                return redirect(reverse('view_income_stream_from_range') + f'?ref_code={encrypted_ref_code}')
            
        return render(request, 'payments/account/show-account-record.html', context)
    except ObjectDoesNotExist:
         messages.info(request, f'No record with ref_code {ref_code} was not found', extra_tags='info')
         return redirect('view_income_stream')
    


@login_required
@department_required(['Account']) 
def approve_income(request):
    if request.method == "POST":
        if 'ref_code' in request.POST:
            ref_code_id = request.POST.get('ref_code')
            
            try:
                income_record = IncomeRecord.objects.filter(ref_code=ref_code_id).first()
                ApprovedIncomeRecord.objects.create(ref_code=income_record, status=True)
                return JsonResponse({'success': 'Income Record Has Been Approved'}, status=200)
            except IncomeRecord.DoesNotExist:
                 return JsonResponse({'error': 'Income Record Does Not Exist'}, status=404)
        return JsonResponse({'error': 'Invalid Parameter'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)




@login_required
@department_required(['Audit', 'Billing', 'Ceo']) 
def generate_bill_report(request):
    return render(request, 'audit/search.html')



# Function to handle form submission for generating report for today
def generate_today_report():
    today = date.today()
    data = Billing.objects.filter(payment_date=today, payment_status=1)
    return data

# Function to handle form submission for generating report for all time
def generate_all_time_report():
    data = Billing.objects.filter(payment_status=1)
    return data

# Function to handle form submission for generating report for a date range
def generate_date_range_report(from_date, to_date):
    data = Billing.objects.filter(payment_date__range=[from_date, to_date], payment_status=1)
    return data


# Function to handle form submission for generating report for a date range and service type
def generate_payment_type_report(service_type, from_date, to_date):
    data = Billing.objects.filter(service_type=service_type, payment_date__range=[from_date, to_date], payment_status=1)
    return data

 
    
@login_required
@department_required(['Audit', 'Billing', 'Ceo']) 
def generated_bill_report(request):
    if request.method == 'POST':
        if 'today' in request.POST:
            try:
                today = date.today()
                formatted_date = today.strftime("%dth %B, %Y")
                report = generate_today_report()
                total_amount = report.aggregate(total_amount=Sum('total_amount'))['total_amount']
                context = {'report': report, 'for': f"Today - {formatted_date}",'total_amount': total_amount}
                return render(request, 'audit/report-result.html', context)
            except ObjectDoesNotExist:
                messages.error(request, 'Invalid search parameter', extra_tags='danger')
                return redirect('generate_bill_report')
        elif 'all_time' in request.POST:
            try:
                report = generate_all_time_report()
                total_amount = report.aggregate(total_amount=Sum('total_amount'))['total_amount']
                context = {'report': report, 'for': 'All Time', 'total_amount': total_amount}
                return render(request, 'audit/report-result.html', context)
            except ObjectDoesNotExist:
                messages.error(request, 'Invalid search parameter', extra_tags='danger')
                return redirect('generate_bill_report')
        elif 'date_range' in request.POST:
            try:
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

                # Format the dates
                formatted_from_date = from_date_obj.strftime("%dth %B, %Y")
                formatted_to_date = to_date_obj.strftime("%dth %B, %Y")
                report = generate_date_range_report(from_date, to_date)
                total_amount = report.aggregate(total_amount=Sum('total_amount'))['total_amount']
                context = {'report': report, 'range': f'{formatted_from_date} - {formatted_to_date}', 'total_amount': total_amount }
                return render(request, 'audit/report-result.html', context)
            except ObjectDoesNotExist:
                messages.error(request, 'Invalid search parameter', extra_tags='danger')
                return redirect('generate_bill_report')
        elif 'payment_type' in request.POST:
            try:
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                payment_type = request.POST.get('service_type')
                                
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

                # Format the dates
                formatted_from_date = from_date_obj.strftime("%dth %B, %Y")
                formatted_to_date = to_date_obj.strftime("%dth %B, %Y")
                report = generate_payment_type_report(payment_type, from_date, to_date)
                total_amount = report.aggregate(total_amount=Sum('total_amount'))['total_amount']
                context = {'report': report, 'range': f'{formatted_from_date} - {formatted_to_date}', 'total_amount': total_amount }
                return render(request, 'audit/report-result.html', context)
            except ObjectDoesNotExist:
                messages.error(request, 'Invalid search parameter', extra_tags='danger')
                return redirect('generate_bill_report')
        else:
            return redirect('generate_bill_report')
    else:
        return redirect('generate_bill_report')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 
@login_required
# def change_password(request):
    
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important to keep the user logged in
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')  # Redirect to the same page after successful password change
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'new-password.html', {'form': form})


# def change_password(request):
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.POST)
#         if form.is_valid():
#             # Process form data
#             new_password = form.cleaned_data['new_password']
#             confirm_password = form.cleaned_data['confirm_password']
            
#             if not new_password  or confirm_password:
#                 messages.error(request, 'All fields are required', extra_tags='danger')
#                 return redirect('change_password')
#             if new_password != confirm_password:
#                 messages.error(request, 'Password do not match', extra_tags='danger')
#                 return redirect('change_password')
              
#             user = form.save()
#             update_session_auth_hash(request, user)
#     else:
#         form = ChangePasswordForm()
    
#     return render(request, 'new-password.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match', extra_tags='danger')
                return redirect('change_password')
            else:
                # Change the password for the user
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'new-password.html', {'form': form})
 
# def reset_password(request):
#     if request.method == 'POST':
#         form = RestPasswordForm(request.POST)
#         if form.is_valid():
#             new_password = form.cleaned_data['new_password']
#             confirm_password = form.cleaned_data['confirm_password']
            
            
#             try:
#                 username = form.cleaned_data['username']
            
#                 if new_password != confirm_password:
#                     messages.error(request, 'Passwords do not match', extra_tags='danger')
#                     return redir    ect('reset_password')
#                 else:
#                     # Change the password for the user
#                     request.user.set_password(new_password)
#                     request.user.save()
#                     update_session_auth_hash(request, username)
#                     messages.success(request, 'Password updated successfully')
#                     return redirect('reset_password')
#             except ObjectDoesNotExist:
#                 messages.error(request, f'Staff with staff ID {username} not found', extra_tags='danger')
#                 return redirect('reset_password')
#     else:
#         form = RestPasswordForm()
    
#     return render(request, 'staff/reset-password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            username = form.cleaned_data['username']
            
            try:
                user = Staff.objects.get(username=username)
            except ObjectDoesNotExist:
                messages.error(request, f'Staff with username {username} not found', extra_tags='danger')
                return redirect('reset_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match', extra_tags='danger')
                return redirect('reset_password')
                
            # Change the password for the user
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset was successfully')
            return redirect('reset_password')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'staff/reset-password.html', {'form': form})
 
 

 
 
 
 
def custom_404(request, exception):
    return render(request, '404.html', {'exception': exception}, status=404)