from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/', views.detail_view, name='detail'),
    path('available/', views.available, name='available'),
    path('qr/', views.qr, name='qr'),
    path('slot/', views.slot, name='slot'),
    path('outpass/', views.outpass, name='outpass'),
    path("user/", views.user, name="user"),
    path('save_slot/', views.save_slot, name='save_slot'),
    path('remove-user/<int:user_id>/', views.remove_user, name='remove-user'),
    path('user-details/<int:user_id>/', views.user_details, name='user_details'),
    path('logout-user/<int:user_id>/', views.logout_user, name='logout_user')

    
]
