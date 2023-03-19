from django.urls import path
from .views import RegisterView, ListRegisterView, BookingDetail, ListPastRegisterView, PastBookingDetail

urlpatterns = [
  path('register/',RegisterView.as_view()),
  path('list/',ListRegisterView.as_view()),
  path('list/<int:pk>/',BookingDetail.as_view()),
  path('list/past/',ListPastRegisterView.as_view()),
  path('list/past/<int:pk>/',PastBookingDetail.as_view()),
]