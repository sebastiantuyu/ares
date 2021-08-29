from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path('users/',include('users.urls')),
    path('preferences/',include('preferences.urls'))
]