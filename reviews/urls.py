from django.urls import path
from . import views

urlpatterns = [
    path('submit_review/', views.submit_review, name='submit_review'),
    path('thank_you/', views.thank_you, name='thank_you'),
]
