from django.test import TestCase
from django.contrib.auth.models import User

from .models import Activity, Shoe, Location, Lap, Point

class ActivityTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='test')

        location = Location.objects.create(creator=self.user, name='test location', longitude=0.0, latitude=0.0)
        shoe = Shoe.objects.create(creator=self.user, manufacturer='test', brand='test')
        activity = Activity.objects.create(creator=self.user, location=location, shoe=shoe)

        for lap_number in range(1, 5):
            lap = Lap.objects.create(creator=self.user, activity=activity, number=lap_number)
            for point in range(100):
                Point.objects.create(creator=self.user, lap=lap)

    def test_activity_details(self):
        ''' Makes sure the activity returns the right details.
        '''
        activity = Activity.objects.first()
        self.assertEqual(activity.creator, self.user)
