from django.urls import path

from .views import LocationCreateView, ActivityCreateView

urlpatterns = [
    path('create/location', LocationCreateView.as_view(), name='create-location'),
    path('create/activity', ActivityCreateView.as_view(), name='create-activity'),
]
