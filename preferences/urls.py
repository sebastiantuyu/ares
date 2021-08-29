from django.urls import path
from .views import *

urlpatterns = [
    path('get-all/',GetPreferences.as_view()),
    path('set-lang/',SetLanguage.as_view()),
    path('delete-lang/',DeleteLanguage.as_view()),
    path('set-preference/',SetPreference.as_view()),
    path('delete-preference/',DeleteLanguage.as_view()),
]