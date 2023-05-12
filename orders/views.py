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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from reportlab.pdfgen import canvas
from django.http import HttpResponse 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Sum
from datetime import timedelta
from rest_framework.views import APIView
from django.db.models.functions import ExtractMonth, ExtractYear
import calendar

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

class SalesOverview(APIView):
    def get(self, request, format = None):

        filter_option = request.query_params.get('filter_option', 'This year')

        if filter_option == 'This year':

            # Get the sales of data for the last 12 months
            today = datetime.today()
            last_12_months = today - timedelta(days=365)
            monthly_sales = Order.objects.annotate(month=ExtractMonth('ordered_date'))\
                                        .filter(ordered_date__gte=last_12_months)\
                                        .values('month')\
                                        .annotate(total_sales=Sum('total_price'))\
                                        .order_by('month')

            #  Create the sales data array for the frontend
            sales_data = []
            for i in range(1, 13):
                month_sales = next((item for item in monthly_sales if item['month'] == i), {'total_sales': 0})
                sales_data.append({
                    'name': calendar.month_name[i][:3],
                    'sales': month_sales['total_sales']
                })

        elif filter_option == 'All time':
            # Get the sales of data for all years
            yearly_sales = Order.objects.annotate(year=ExtractYear('ordered_date'))\
                                .values('year')\
                                .annotate(total_sales=Sum('total_price'))\
                                .order_by('year')
            
            # Create the sales data array for the frontend
            sales_data = []
            for year_sale in yearly_sales:
                sales_data.append({
                    'name': str(year_sale['year']),
                    'sales': year_sale['total_sales']
                })

        # Get the total sales
        total_sales = Order.objects.all().aggregate(Sum('total_price'))['total_price__sum'] or 0
        # Get the total orders
        total_orders = Order.objects.all().count()
        
        # Get the total sales for today
        today = datetime.today()
        today_sales = Order.objects.filter(ordered_date__gte=today).aggregate(Sum('total_price'))['total_price__sum'] or 0
        # Get the total sales for yesterday
        yesterday = datetime.today() - timedelta(days=1)
        yesterday_sales = Order.objects.filter(ordered_date__gte=yesterday).aggregate(Sum('total_price'))['total_price__sum'] or 0
        # Get the total sales for the last 7 days
        last_7_days = datetime.today() - timedelta(days=7)
        last_7_days_sales = Order.objects.filter(ordered_date__gte=last_7_days).aggregate(Sum('total_price'))['total_price__sum'] or 0
        # Get the total sales for the last 30 days
        last_30_days = datetime.today() - timedelta(days=30)
        last_30_days_sales = Order.objects.filter(ordered_date__gte=last_30_days).aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Get the total sales for the last 365 days
        last_365_days = datetime.today() - timedelta(days=365)
        last_365_days_sales = Order.objects.filter(ordered_date__gte=last_365_days).aggregate(Sum('total_price'))['total_price__sum'] or 0

        response = {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'today_sales': today_sales,
            'yesterday_sales': yesterday_sales,
            'last_7_days_sales': last_7_days_sales,
            'last_30_days_sales': last_30_days_sales,
            'last_365_days_sales': last_365_days_sales,
            'sales_data': sales_data
        }

        return Response(response)
    
        


def generate_pdf(request, order_id):
    # Retrieve the order from the database based on the order_id parameter
    order = Order.objects.get(order_id=order_id)

    # Generate the PDF file using ReportLab
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer)
    pdf_canvas.setPageSize((400, 600))

    # Set font sizes and positions for different elements
    title_size = 10
    title_pos = 200
    header_size = 8
    header_pos = 500
    item_header_pos = 440
    item_size = 8
    item_pos = 420
    item_space = 10


    # Draw the title
    pdf_canvas.setFontSize(title_size)
    pdf_canvas.drawCentredString(title_pos, 550, 'Order Receipt')

    # Draw the order details
    pdf_canvas.setFontSize(header_size)
    pdf_canvas.drawString(50, header_pos, f'Order ID: {order_id}')
    pdf_canvas.drawString(50, header_pos - item_space, f'Customer Name: {order.user_name}')
    pdf_canvas.drawString(50, header_pos - item_space * 2, f'Table No: {order.table_no}')
    pdf_canvas.drawRightString(350, header_pos, f'Ordered Time: {order.ordered_date}')
    pdf_canvas.drawRightString(350, header_pos - item_space, f'Ordered Time: {datetime.strptime(str(order.ordered_time), "%H:%M:%S.%f").strftime("%I:%M %p")}')
    pdf_canvas.drawRightString(350, header_pos - item_space * 2, f'Payment Method: {order.payment_method}')

    # Add the ordered items to the PDF
    pdf_canvas.setFontSize(title_size)
    pdf_canvas.drawString(50, item_header_pos, 'Ordered Items')
    pdf_canvas.line(50, item_header_pos - 10, 350, item_header_pos - 10)
    pdf_canvas.setFontSize(item_size)
    y = item_pos
    pdf_canvas.drawString(55, y, 'Item')
    pdf_canvas.drawString(260, y, 'Qty')
    pdf_canvas.drawString(310, y, 'Price')

    y -= item_space
    pdf_canvas.line(50, y, 350, y)
    y -= 15

    for item in order.items.all():
        pdf_canvas.drawString(50, y, f' {item.food_id.food_name}')
        pdf_canvas.drawString(260, y, f' {item.quantity}')
        pdf_canvas.drawString(310, y, f' Rs. {item.food_id.food_price}')
        y -= item_space + 15

    pdf_canvas.line(50, y, 350, y)
    y -= 15
    pdf_canvas.setFontSize(item_size)
    pdf_canvas.drawString(50, y, 'Total')
    pdf_canvas.drawRightString(330, y, f' Rs. {order.total_price}')

    pdf_canvas.drawString(150, y - item_space * 3, 'Thank you for your order!')

    # Close the PDF object cleanly, and we're done.
    pdf_canvas.showPage()
    pdf_canvas.save()

    return HttpResponse(buffer.getvalue(), content_type='application/pdf')


@api_view(['GET'])
def download_pdf(request, order_id):
    pdf_response = generate_pdf(request, order_id)

    return pdf_response

@csrf_exempt
@api_view(['POST'])
def send_email(request, order_id):
    pdf = generate_pdf(request, order_id)


    # Send the email with the PDF attachment
    email = request.data.get('email')
    print(email)
    msg = EmailMessage(
        f'Order Receipt - {order_id}',
        'Please find the attached order receipt',
        settings.EMAIL_HOST_USER,
        [email]
    )
    msg.attach(f'order_{order_id}.pdf', pdf.getvalue(), 'application/pdf')
    msg.send()

    return JsonResponse({'success': True})




def accept_order(request, order_id):
    # Accept the order and update the status in the database
    # ...
    
    # Send a message to the user's cart channel with the new status
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        order_id,
        {
            'type': 'order_status',
            'order_status': 'Accepted'
        },
        {
            'type': 'order_status',
            'order_status': 'Rejected'
        }
    )

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
        response = requests.post('https://khalti.com/api/v2/payment/initiate/', json=payload, headers=headers)
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
