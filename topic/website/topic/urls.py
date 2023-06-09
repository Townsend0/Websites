from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact/', views.contact, name = 'contact'),
    path('topics-detail/<int:card_id>', views.detail, name = 'detail'),
    path('topics-listing/', views.listing, name = 'listing'),
]
