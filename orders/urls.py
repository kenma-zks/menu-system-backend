from django.urls import path
from .views import OrderList, OrderDetail, OrderedItemList, OrderedItemDetail, PaymentTokenView, PaymentVerificationView, generate_pdf, download_pdf, send_email, SalesOverview

urlpatterns = [
    path('order/', OrderList.as_view()),
    path('order/<int:pk>/', OrderDetail.as_view()),
    path('ordereditem/', OrderedItemList.as_view()),
    path('ordereditem/<int:pk>/', OrderedItemDetail.as_view()),
    path('payment/token/', PaymentTokenView.as_view(), name='payment_token'),
    path('payment/verify/', PaymentVerificationView.as_view(), name='payment_verify'),
    path('order/pdf/<int:order_id>/', download_pdf, name='download_pdf'),
    path('order/email/<int:order_id>/', send_email, name='send_email'),
    path('sales/', SalesOverview.as_view(), name='sales_overview'),
]
