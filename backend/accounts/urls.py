
from django.urls import path
from .views import LoginView, MeView

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
   
    path('auth/me/', MeView.as_view()),
]
