from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('api/kobo-webhook/', views.kobo_webhook, name='kobo_webhook'),
    path('api/kobo-webhook/', views.save_all_data, name='save_all_data'),
    path('show-details/', views.show_details, name='show_details'),

    # api for the crude operation in react js
    path('api/user/create/', views.create_user, name='create_user'),
    path("api/user/update/<int:user_id>/", views.update_user, name='update_user'),
    path('api/user/details/', views.user_details, name='user_details'),
    path('api/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
]
