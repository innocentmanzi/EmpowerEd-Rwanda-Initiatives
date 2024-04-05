from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('change-password/', views.change_password, name='change_password'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('profile', views.profile, name='profile'),
    path('settings', views.user_settings, name='settings'),
]