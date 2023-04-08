from django.urls import path
from .views import UserAccountList, UserDetail, LogoutView, RegisterView, MyTokenObtainPairView, forgot_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('<int:pk>/', UserDetail.as_view()),
    path('', UserAccountList.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', forgot_password, name='forgot-password')
]