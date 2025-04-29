from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.cargo_registration, name='registration'),
    path('cargo-update/', views.cargo_update, name='cargo_update'),
    path('cargo/<int:cargo_id>/', views.cargo_detail, name='cargo_detail'),
    path('generate-invoice/<int:cargo_id>/', views.generate_invoice, name='generate_invoice'),
    path('reports/', views.reports, name='reports'),
    path('download-invoice/<int:invoice_id>/', views.download_invoice, name='download_invoice'),
    path('faq/', views.faq, name='faq'),
]