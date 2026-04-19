from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('api/kobo-webhook/', views.kobo_webhook, name='kobo_webhook'),
    path('api/kobo-webhook/', views.save_all_data, name='save_all_data'),
    path('show-details/', views.show_details, name='show_details')

]
