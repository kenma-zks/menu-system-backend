from django.urls import path
from .views import SubAdminAccountList, SubAdminAccountDetail, LoginView, LogoutView, RegisterView, UserView

urlpatterns = [
    path('<int:pk>/', SubAdminAccountDetail.as_view()),
    path('', SubAdminAccountList.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
]