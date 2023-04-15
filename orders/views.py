from django.shortcuts import render
from rest_framework import generics
from .serializers import OrderSerializer, OrderedItemSerializer
from .models import Order, OrderedItem
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests

# Create your views here.

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrderedItemList(generics.ListCreateAPIView):
    queryset = OrderedItem.objects.all()
    serializer_class = OrderedItemSerializer

class OrderedItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderedItem.objects.all()
    serializer_class = OrderedItemSerializer

class PaymentTokenView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount', None)
        if amount is None:
            return JsonResponse({'error': 'Amount is required'})

        headers = {
            'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
        }
        payload = {
            'amount': request.POST.get('amount'),
            'mobile': request.user.phone_number,
            'product_identity': 'my-unique-product-identifier',
            'product_name': 'Mero Menu',
            'product_url': 'http://localhost:5173/',

        }
        response = requests.post('https://a.khalti.com/api/v2/payment/initiate/', json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        return JsonResponse({'token': data['token']})

class PaymentVerificationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        token = request.POST.get('token', None)
        if token is None:
            return JsonResponse({'error': 'Token is required'})

        headers = {
            'Authorization': f'Key {settings.TEST_SECRET_KEY}',
        }
        payload = {
            'token': token,
        }
        response = requests.post('https://khalti.com/api/v2/payment/verify/', json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        # handle the response as per your requirement
        return JsonResponse({'status': 'success', 'data': data})


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateOrderPaid(request, pk):
#     order = Order.objects.get(order_id=pk)

#     if request.method == 'PUT':
#         payment_method = request.data.get('payment_method')
#         payment_result = request.data.get('paymentResult')

#         if not payment_method or not payment_result:
#             return Response({'error': 'Payment method and result are required'})

#         if payment_method == 'Khalti':
#             headers = {
#                 'Authorization': f"Key {settings.TEST_SECRET_KEY}"
#             }
#             payload = {
#                 'token': payment_result.get('token'),
#                 'amount': payment_result.get('amount'),
#             }

#             try:
#                 response = requests.post('https://khalti.com/api/v2/payment/verify/', data=payload, headers=headers)

#                 if response.status_code == 200:
#                     response_json = response.json()

#                     if response_json.get('idx'):
#                         order.payment_method = payment_method
#                         order.order_status = 'Paid'
#                         order.save()
#                         return Response({'message': 'Order was paid.'})
#                     else:
#                         return Response({'error': 'Payment verification failed'})
#                 else:
#                     return Response({'error': 'Khalti API request failed'})
#             except Exception as e:
#                 return Response({'error': str(e)})

#         # Add other payment methods here
#         else:
#             return Response({'error': 'Invalid payment method'})

#     return Response({'error': 'Invalid request method'})
