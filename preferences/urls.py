from django.urls import path
from .views import *

urlpatterns = [
    path('set/',SetPreference.as_view()),
    path('delete/',DeletePreference.as_view()),
    path('get-all/',GetPreferences.as_view()),
    path('lang/all/',AllLanguages.as_view()),
    path('lang/set/',SetLanguage.as_view()),
    path('lang/delete/',DeleteLanguage.as_view()),
    path('lang/update/',UpdateLanguageLevel.as_view()),
]