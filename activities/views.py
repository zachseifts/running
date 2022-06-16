from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import ActivityCreateForm, LocationCreateForm, ShoeCreateForm
from .models import Activity, Lap, Point, Location, Shoe

import fitdecode

class LocationCreateView(LoginRequiredMixin, View):
    ''' A view for creating a new location.
    '''
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    form_class = LocationCreateForm
    form_redirect = '/accounts/profile/' # change to reverse_lazy('home')
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
                creator=request.user,
                latitude=form.cleaned_data['latitude'],
                longitude=form.cleaned_data['longitude'])
            location.save()
            messages.add_message(request, messages.INFO, 'Added location: {}'.format(name))
            return HttpResponseRedirect(self.form_redirect)

        return render(request, self.template_name, {'form': form})


class ActivityCreateView(LoginRequiredMixin, View):
    ''' A view that creates a new activity.
    '''
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    form_class = ActivityCreateForm
    form_redirect = '/accounts/profile/'
    template_name = 'create-activity.html'

    def get(self, request):
        form = self.form_class()
        form.fields['location'].queryset = Location.objects.filter(creator=request.user)
        form.fields['shoe'].queryset = Shoe.objects.filter(creator=request.user).filter(is_active=True)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            lap_number = 1
            activity = Activity(
                creator = request.user,
                location = form.cleaned_data['location'],
                notes = form.cleaned_data['notes'],
                sport = form.cleaned_data['sport'],
                shoe = form.cleaned_data['shoe'],
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

                                try:
                                    heart_rate = frame.get_value('heart_rate')
                                except KeyError:
                                    heart_rate = 0

                                point = Point(
                                    creator = request.user,
                                    lap=lap,
                                    timestamp=frame.get_value('timestamp'),
                                    longitude=longitude,
                                    latitude=latitude,
                                    altitude=altitude,
                                    speed=frame.get_value('speed'),
                                    cadence=frame.get_value('cadence'),
                                    heart_rate = heart_rate,
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


class ActivityDetailView(LoginRequiredMixin, View):
    ''' View the details of an activitiy.
    '''
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    template_name = 'activity.html'

    def get(self, request, **kwargs):
        activity_id = kwargs.get('activity_id')
        try:
            activity = Activity.objects.get(pk=activity_id)

            times = list()
            cadence = list()
            speed = list()
            heart_rate = list()
            altitude = list()

            for lap in activity.lap_set.all():
                for point in lap.point_set.all():
                    times.append(point.timestamp.strftime('%H:%M:%S'))
                    cadence.append(point.cadence)
                    speed.append(point.speed)
                    heart_rate.append(point.heart_rate)
                    altitude.append(point.altitude)

        except Activity.DoesNotExist:
            raise Http404("Activity does not exist")

        context = {
            'activity': activity,
            'times': times,
            'cadence': cadence,
            'speed': speed,
            'heart_rate': heart_rate,
            'altitude': altitude,
        }
        return render(request, self.template_name, context)


class ShoeCreateView(LoginRequiredMixin, View):
    ''' A view for creating a new location.
    '''
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    form_class = ShoeCreateForm
    form_redirect = '/'
    template_name = 'create-shoe.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            manufacturer = form.cleaned_data['manufacturer']
            brand = form.cleaned_data['brand']
            shoe = Shoe(
                brand=brand,
                manufacturer=manufacturer,
                creator=request.user)
            shoe.save()
            messages.add_message(request, messages.INFO, 'Added new shoe: {} {}'.format(manufacturer, brand))
            return HttpResponseRedirect(self.form_redirect)

        return render(request, self.template_name, {'form': form})

