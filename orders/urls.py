from django.urls import path
from .views import OrderList, OrderDetail, OrderedItemList, OrderedItemDetail

urlpatterns = [
    path('order/', OrderList.as_view()),
    path('order/<int:pk>/', OrderDetail.as_view()),
    path('ordereditem/', OrderedItemList.as_view()),
    path('ordereditem/<int:pk>/', OrderedItemDetail.as_view()),
]
