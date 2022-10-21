from django.urls import path

from .views import LocationCreateView
from .views import ActivityCreateView
from .views import ActivityDetailView
from .views import ShoeCreateView
from .views import ActivityWeeklyView
from .views import ActivityYearlyView

urlpatterns = [
    path('new/location', LocationCreateView.as_view(), name='new-location'),
    path('new/activity', ActivityCreateView.as_view(), name='new-activity'),
    path('new/shoe', ShoeCreateView.as_view(), name='new-shoe'),
    path('detail/<int:activity_id>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('<int:year>', ActivityYearlyView.as_view(), name='activity-yearly'),
    path('<int:year>/<int:week>', ActivityWeeklyView.as_view(), name='activity-weekly'),
]
