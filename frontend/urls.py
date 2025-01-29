from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payments/', views.payments, name='payments'),
    path('documents/', views.documents, name='documents'),
    path('notifications/', views.notifications, name='notifications'),
] 