from datetime import timedelta

from django.views import View
from django.shortcuts import render
from django.utils.timezone import now

from activities.models import Location, Activity, Shoe
from activities.utils import generate_stats

class HomeView(View):
    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            context['locations'] = Location.objects.filter(creator=request.user)
            context['activities'] = Activity.objects.filter(creator=request.user).order_by('-created')
            context['shoes'] = Shoe.objects.filter(creator=request.user).filter(is_active=True)

            year, week, _ = now().isocalendar()
            month = now().month

            context['weekly'] = Activity.objects.filter(created__year=year, created__week=week).order_by('-created')
            weekly_stats = generate_stats('weekly', context['weekly'])
            context = context | weekly_stats

            context['monthly'] = Activity.objects.filter(created__year=year, created__month=month).order_by('-created')
            monthly_stats = generate_stats('monthly', context['monthly'])
            context = context | monthly_stats

            context['yearly'] = Activity.objects.filter(created__year=year).order_by('-created')
            yearly_stats = generate_stats('yearly', context['yearly'])
            context = context | yearly_stats

        return render(request, 'home.html', context)
