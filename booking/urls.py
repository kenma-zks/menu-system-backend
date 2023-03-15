from django.urls import path
from .views import RegisterView, ListRegisterView, BookingDetail

urlpatterns = [
  path('register/',RegisterView.as_view()),
  path('list/',ListRegisterView.as_view()),
  path('list/<int:pk>/',BookingDetail.as_view()),
]