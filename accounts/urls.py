from django.urls import path

from django.contrib.auth import views

from .views import AccountsProfileView

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'), name='accounts-login'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='accounts-logout'),
    path('profile/', AccountsProfileView.as_view(), name='accounts-profile'),
]
