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
            lap = Lap.objects.create(creator=self.user,
                activity=activity,
                number=lap_number,
                total_distance=1000,
                )
            for point in range(100):
                Point.objects.create(creator=self.user,
                    lap=lap,
                    speed=point,
                    altitude=point*100,
                    heart_rate=point*10)

    def test_activity_start(self):
        ''' Makes sure the start() function returns a point object.
        '''
        activity = Activity.objects.first()
        start = activity.start()
        self.assertIsInstance(start, Point)
        self.assertEqual(start.id, 1)

    def test_activity_end(self):
        ''' Makes sure the end() function returns a point object.
        '''
        activity = Activity.objects.first()
        end = activity.end()
        self.assertIsInstance(end, Point)
        self.assertEqual(end.id, 400)

    def test_duration(self):
        pass

    def test_activity_get_points(self):
        ''' Makes sure the get_points() function returns a list of tracks.
        '''
        activity = Activity.objects.first()
        points = activity.get_points()
        self.assertTrue(len(points) > 0)

    def test_get_total_distance(self):
        ''' Makes sure that the get_total_distance() function returns a valid
        value. '''
        activity = Activity.objects.first()
        distance = activity.get_total_distance()
        self.assertEqual(distance, 2.4860161591050343)

    def test_get_max_speed(self):
        ''' Makes sure that the get_max_speed() function returns a valid
        value. '''
        activity = Activity.objects.first()
        max_speed = activity.get_max_speed()
        self.assertEqual(max_speed, 99.0)

    def test_get_avg_speed(self):
        ''' Makes sure that the get_avg_speed() function returns a valid
        value. '''
        activity = Activity.objects.first()
        avg_speed = activity.get_avg_speed()
        self.assertEqual(avg_speed, 49.5)

    def test_get_max_altitude(self):
        ''' Makes sure that the get_total_distance() function returns a valid
        value. '''
        activity = Activity.objects.first()
        max_altitude = activity.get_max_altitude()
        self.assertEqual(max_altitude, 9900.0)

    def test_get_max_heart_rate(self):
        ''' Makes sure that the get_total_distance() function returns a valid
        value. '''
        activity = Activity.objects.first()
        heart_rate = activity.get_max_heart_rate()
        self.assertEqual(heart_rate, 990)

    def test_get_minutes_per_mile(self):
        pass

