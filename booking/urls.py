from django.urls import path
from .views import RegisterView, ListRegisterView

urlpatterns = [
  path('register/',RegisterView.as_view()),
  path('list/',ListRegisterView.as_view()),
]