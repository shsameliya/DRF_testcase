from django.urls import path
from cardekho_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('list',views.car_list_view,name='car_list'),
    path('register',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('dashboard',views.DashboardView.as_view(),name='dashboard'),
    path('user/<int:id>', views.UserDetailView.as_view(), name='userdetail'),
    path('delete/<int:id>', views.UserDeleteView.as_view(), name='userdelete'),
    path('users', views.UserListView.as_view(), name='userlist'), 
    path('<int:pk>',views.car_detail_view,name='car_detail')
]