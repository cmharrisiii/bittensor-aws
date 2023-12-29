from django.urls import path
from bittensor_api import views

urlpatterns = [
    path('/prompt',views.prompting)
]