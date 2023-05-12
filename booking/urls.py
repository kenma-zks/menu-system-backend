from django.urls import path
from .views import RegisterView, ListRegisterView, BookingDetail, ListPastRegisterView, PastBookingDetail, send_email

urlpatterns = [
  path('register/',RegisterView.as_view()),
  path('list/',ListRegisterView.as_view()),
  path('list/<int:pk>/',BookingDetail.as_view()),
  path('list/past/',ListPastRegisterView.as_view()),
  path('list/past/<int:pk>/',PastBookingDetail.as_view()),
  path('email/',send_email),
]