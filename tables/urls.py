from django.urls import path
from .views import TableDetail, TableList

urlpatterns = [
    path('table/', TableList.as_view()),
    path('table/<int:pk>/', TableDetail.as_view()),
]