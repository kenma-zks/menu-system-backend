from django.urls import path

from .views import FoodCategoryList, FoodCategoryDetail, FoodDetailsList, FoodDetailsDetail

urlpatterns = [
    path('foodcategory/', FoodCategoryList.as_view()),
    path('foodcategory/<int:pk>/', FoodCategoryDetail.as_view()),
    path('fooddetails/', FoodDetailsList.as_view()),
    path('fooddetails/<int:pk>/', FoodDetailsDetail.as_view()),  
]