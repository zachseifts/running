from django.urls import path

from .views import LocationCreateView, ActivityCreateView, ActivityDetailView

urlpatterns = [
    path('create/location', LocationCreateView.as_view(), name='create-location'),
    path('create/activity', ActivityCreateView.as_view(), name='create-activity'),
    path('<int:activity_id>/', ActivityDetailView.as_view(), name='activity-detail'),
]
