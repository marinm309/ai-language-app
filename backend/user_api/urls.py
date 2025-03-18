from django.urls import path
from . import views

urlpatterns = [
    path('user', views.UserView.as_view(), name='user'),
    path('user/<int:pk>', views.SingleUserView.as_view(), name='single-user'),
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
]
