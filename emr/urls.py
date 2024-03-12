from django.urls import path,re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.user_login, name="login"),
    re_path(r'^logout/?$', views.logout, name="logout"),
    re_path(r'^change_password/?$', views.change_password, name="change_password"),
    re_path(r'^secure/?$', views.dashboard, name="dashboard"),
    re_path(r'^staff/search/?$', views.search_staff, name="search_staff"),
    path('staff/<int:id>/', views.view_staff, name='view_staff'),
    re_path(r'^staff/add_staff/?$', views.add_staff, name="add_staff"),
    
    re_path(r'^patients/?$', views.get_patients, name="get_patients"),
    path("patient/search", views.search_patient, name="search_patient"),
    re_path(r'^patients/(?P<user_id>\d+)/?$', views.get_patient, name="get_patient"),
    path("patients/register-card/", views.register_search_card, name="register_search_card"),
    re_path(r'^patients/register/?$', views.add_patient, name="register_patient"),
    re_path(r'^patients/(?P<user_id>\d+)/edit/?$', views.update_patient, name="update_patient"),
    re_path(r'^add_vital/(?P<appointment_id>\d+)/?$', views.add_vital, name="add_vital"),
    re_path(r'^add_vital/?$', views.appointments),
    
    path("add_vital/<int:appointment_id>/<int:patient_id>", views.add_vital, name="add_vital"),
    re_path(r'^appointments/?$', views.appointments, name="appointments"),
    re_path(r'^appointments/(?P<user_id>\d+)/?$', views.book_appointment, name="book_appointment"),
    re_path(r'^appointments/(?P<user_id>\d+)/(?P<appointment_id>\d+)/?$', views.book_appointment_doctor, name="book_appointment_doctor"),
    path('appointments/scheduled', views.scheduled_appointments, name='scheduled_appointments'),

     
    path('billing/', views.home),
    re_path(r'^billing/payments/?$', views.payments, name="payment_history"),
    path('billing/consultation/<str:status>/', views.consultation_payments, name='consultation_payments'),
    path('billing/lab/<str:status>/', views.lab_payments, name='lab_payments'),
    path('billing/pharmacy/<str:status>/', views.drug_payments, name='drug_payments'),
    path('billing/confirm/<int:billing_id>/', views.confirm_appointment_payment, name='confirm_appointment_payment'),
    path('billing/confirm-drug/<int:order_id>/', views.confirm_drug_payment, name='confirm_drug_payment'),
    path('billing/invoice/<int:qid>/', views.invoice, name='invoice'),
    path('billing/card-registration/', views.card_registration_payment, name='pay_card'),
    path('billing/card-renewal/', views.card_renewal_payment, name='card_renewal_payment'),
    path('billing/add-card-price/', views.add_card_price, name='add_card_price'),
    path("billing/card/search", views.card_payment_search, name="card_payment_search"),
    path("billing/income-stream/create", views.create_income_stream, name="create_income_stream"),
    path("billing/income-streams", views.income_streams, name="income_streams"),
    path("billing/income-streams/record", views.record_income_stream, name="record_income_stream"),
    path("billing/income-streams/search", views.view_income_stream, name="view_income_stream"),
    path("billing/income-streams/show", views.view_income_stream_from_range, name="view_income_stream_from_range"),
    re_path(r'^billing/confirm_payment/?$', views.confirm_payment, name="confirm_payment"),
    
    path("account/income/action", views.approve_income, name="approve_income"),
    
    
    

    
    
    path('lab/', views.home),
    path('lab/add_lab_results/<int:id>/', views.add_lab_result, name='add_lab_result'),
    path('lab/view_result/<int:test_id>/', views.view_lab_result, name='view_lab_result'),
    re_path(r'^lab/lab_results/?$', views.lab_results, name="lab_results"),
    path('lab/add_lab_test/<int:user_id>/', views.add_lab_test, name='add_lab_test'),
    path('lab/lab_test/<int:user_id>/', views.patient_lab_tests, name='patient_lab_tests'),
    path('lab/add_lab_price/', views.add_lab_price, name='add_lab_price'),
    path('lab/view_lab_price/', views.lab_prices, name='lab_prices'),
    re_path(r'^lab/lab_tests/?$', views.lab_list, name="lab_tests"),
    
    path('doctor/', views.home),
    re_path(r'^doctor/appointments/?$', views.appointments, name="doctor_appointments"),
    re_path(r'^doctor/prescriptions/(?P<user_id>\d+)/?$', views.prescriptions, name="prescriptions"),
    re_path(r'^doctor/prescriptions/(?P<user_id>\d+)/(?P<prescription_id>\d+)/?$', views.prescription, name="prescription"),
    path('doctor/prescriptions/create/<int:user_id>/<int:appointment_id>', views.add_prescription, name="add_prescription"),
    
    
    path('pharmacy/', views.home),
    re_path(r'^pharmacy/drugs/?$', views.drug_list, name="drugs"),
    re_path(r'^pharmacy/add_drug/?$', views.add_drug, name="add_drug"),
    path('pharmacy/update_drug/<int:d_id>/', views.update_drug, name='update_drug'),
    re_path(r'^pharmacy/drug_sell/?$', views.drug_sell, name="sale_drug"),
    # re_path(r'^pharmacy/sale_drug/?$', views.sale_drug, name="sale_drug"),
    path('pharmacy/prescribed', views.prescribe_drug, name="prescribed_drug"),
    path('pharmacy/prescribed_drugs/<int:prescription_id>/', views.view_prescribed_drug, name="view_prescribed_drugs"),
    re_path(r'^pharmacy/sale_drug/?$', views.sale_drug, name="sale_drug"),
    path('pharmacy/get_drug_details/', views.get_drug_details, name="get_drug_details"),
    path('pharmacy/drug_history/', views.drugs_history, name="drugs_history"),
    path('pharmacy/history_detail/<int:order>/', views.drug_history_detail, name="drug_history_detail"),
    
    
    
    path('report/generate', views.generate_bill_report, name="generate_bill_report"),
    path('report/generate/result', views.generated_bill_report, name="generated_bill_report"),
    
]
