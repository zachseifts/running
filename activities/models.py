from django.db import models
from django.conf import settings

class Location(models.Model):
    ''' A location where an activity takes place.
    '''

    created = models.DateTimeField('date created', auto_now_add=True, blank=True)
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ''' An activity that takes place.
    '''

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField('date created', auto_now_add=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def start(self):
        ''' Returns the start of this activity.
        '''
        return self.get_gps_tracks()[0]

    def end(self):
        ''' Returns the end of this activity.
        '''
        return self.get_gps_tracks()[-1]

    def get_gps_tracks(self):
        ''' Returns a list of points for this activity.
        '''
        points = list()

        for lap in self.lap_set.all():
            for point in lap.point_set.all():
                points.append(point)

        return points

    def get_total_distance(self):
        ''' Returns the total distance for this activitiy.
        '''
        distances = [lap.total_distance for lap in self.lap_set.all()]
        return sum(distances) / 1609

    def get_max_speed(self):
        speeds = [point.speed for point in self.get_gps_tracks()]
        return max(speeds)

    def get_max_altitude(self):
        altitudes = [point.altitude for point in self.get_gps_tracks()]
        return max(altitudes)


class Lap(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField('date created', auto_now_add=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    total_distance = models.FloatField(default=0, null=True)


class Point(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField('date created', auto_now_add=True, blank=True)
    lap = models.ForeignKey(Lap, on_delete=models.CASCADE, null = True)
    timestamp = models.DateTimeField(null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    altitude = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    cadence = models.IntegerField(default=0, null=True)
    heart_rate = models.IntegerField(default=0, null=True)

