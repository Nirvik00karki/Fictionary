from django.contrib import admin
from django.urls import path
from . import views

app_name = 'novels'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('novel/<int:novel_id>/', views.novel_details, name='novel_details'),
    path('chapter_details/<int:chapter_id>/', views.chapter_details, name='chapter_details'),
    path('novel/<int:novel_id>/add-chapter/', views.add_new_chapter, name='add_new_chapter'),
    path('make_payment/<int:chapter_id>/', views.make_payment, name='make_payment'),
    path('add_to_cart/<int:chapter_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('view_cart/', views.ViewCartView.as_view(), name='view_cart'),
    path('remove_from_cart/<int:chapter_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
