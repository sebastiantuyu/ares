from users.views import GetCoincidences, LogIn, LogInAsGuesst, LogOut, SetMatch
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('login/',LogIn.as_view()),
    path('logout/',LogOut.as_view()),
    path('set-match/',SetMatch.as_view()),
    path('login-as-guesst/',LogInAsGuesst.as_view()),
    path('get-coincidences/',GetCoincidences.as_view()),
]