from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('add/', views.add_contact, name='add_contact'),
    path('<int:pk>/', views.contact_detail, name='contact_detail'),
    path('<int:pk>/add-interaction/', views.add_interaction, name='add_interaction'),
    path('<int:pk>/generate-email/', views.generate_email, name='generate_email'),
]