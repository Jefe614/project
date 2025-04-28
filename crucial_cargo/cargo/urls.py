from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    path('registration/', views.cargo_registration, name='registration'),
    path('cargo-update/', views.cargo_update, name='cargo_update'),
    path('generate-invoice/<int:cargo_id>/', views.generate_invoice, name='generate_invoice'),
    path('reports/', views.reports, name='reports'),
    path('download-invoice/<int:invoice_id>/', views.download_invoice, name='download_invoice'),
    path('faq/', views.faq, name='faq'),
]