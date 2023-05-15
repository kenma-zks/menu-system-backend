from django.urls import path
from .views import OrderList, OrderDetail, OrderedItemList, OrderedItemDetail, verify_payment, generate_pdf, download_pdf, send_email, SalesOverview

urlpatterns = [
    path('order/', OrderList.as_view()),
    path('order/<int:pk>/', OrderDetail.as_view()),
    path('ordereditem/', OrderedItemList.as_view()),
    path('ordereditem/<int:pk>/', OrderedItemDetail.as_view()),
    path('order/verifypayment/', verify_payment, name='verify_payment'),
    path('order/pdf/<int:order_id>/', download_pdf, name='download_pdf'),
    path('order/email/<int:order_id>/', send_email, name='send_email'),
    path('sales/', SalesOverview.as_view(), name='sales_overview'),
]
