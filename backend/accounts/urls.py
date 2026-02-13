from django.urls import path
from .views import LoginView, RegisterView, MeView

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path('auth/me/', MeView.as_view()),
]
