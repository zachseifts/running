from datetime import datetime, timedelta

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import ActivityCreateForm, LocationCreateForm
from .models import Activity, Lap, Point, Location

import fitdecode

class LocationCreateView(View):
    ''' A view for creating a new location.
    '''
    form_class = LocationCreateForm
    form_redirect = '/accounts/profile/'
    template_name = 'create-location.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = Location(
                name=name,
                creator=request.user)
            location.save()
            messages.add_message(request, messages.INFO, 'Added location: {}'.format(name))
            return HttpResponseRedirect(self.form_redirect)

        return render(request, self.template_name, {'form': form})

class ActivityCreateView(View):
    ''' A view that creates a new activity.
    '''
    form_class = ActivityCreateForm
    form_redirect = '/accounts/profile/'
    template_name = 'create-activity.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            lap_number = 1
            activity = Activity(
                creator = request.user,
                location = form.cleaned_data['location'],
                notes = form.cleaned_data['notes'],
            )
            activity.save()
            lap = Lap(
                creator = request.user,
                activity = activity,
                number = lap_number)
            lap.save()
            with fitdecode.FitReader(request.FILES['file']) as fit_file:
                for frame in fit_file:
                    if isinstance(frame, fitdecode.records.FitDataMessage):
                        # Process records
                        if frame.name == 'record':
                            if (frame.has_field('position_lat') and
                                frame.has_field('position_long')):
                                latitude = frame.get_value('position_lat') / ((2**32) / 360)
                                longitude = frame.get_value('position_long') / ((2**32) / 360)
                                altitude = frame.get_value('altitude') * 3.281
                                point = Point(
                                    creator = request.user,
                                    lap=lap,
                                    timestamp=frame.get_value('timestamp'),
                                    longitude=longitude,
                                    latitude=latitude,
                                    altitude=altitude,
                                    speed=frame.get_value('speed'),
                                    cadence=frame.get_value('cadence'),
                                    heart_rate=frame.get_value('heart_rate'),
                                )
                                point.save()
                        if frame.name == 'lap':
                            lap_number += 1
                            lap = Lap(
                                activity=activity,
                                number=lap_number,
                                total_distance = frame.get_value('total_distance'),
                            )
                            lap.save()

            messages.add_message(request, messages.INFO, 'Finished processing .FIT file.')
            return HttpResponseRedirect(self.form_redirect)
        return render(request, self.template_name, {'form': form})


class ActivityDetailView(View):
    template_name = 'activity-detail.html'

    def get(self, request, **kwargs):
        activity_id = kwargs.get('activity_id')
        try:
            activity = Activity.objects.get(pk=activity_id)
        except Activity.DoesNotExist:
            raise Http404("Activity does not exist")

        return render(request, self.template_name, {'activity': activity})

