
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emr.urls'))
]


handler404 = 'emr.views.custom_404'