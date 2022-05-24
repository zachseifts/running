from django.urls import path

from .views import LocationCreateView
from .views import ActivityCreateView
from .views import ActivityDetailView
from .views import ShoeCreateView

urlpatterns = [
    path('create/location', LocationCreateView.as_view(), name='create-location'),
    path('create/activity', ActivityCreateView.as_view(), name='create-activity'),
    path('create/shoe', ShoeCreateView.as_view(), name='create-shoe'),
    path('<int:activity_id>/', ActivityDetailView.as_view(), name='activity-detail'),
]
