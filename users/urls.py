from django.urls import path
from users.views import GetCoincidences, GetMatches, LogIn, LogInAsGuest, LogOut, SetMatch

urlpatterns = [
    path('login/',LogIn.as_view()),
    path('logout/',LogOut.as_view()),
    path('match/set/',SetMatch.as_view()),
    path('match/get/',GetMatches.as_view()),
    path('login-as-guest/',LogInAsGuest.as_view()),
    path('get-coincidences/',GetCoincidences.as_view()),
]