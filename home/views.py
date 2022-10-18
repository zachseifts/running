from datetime import timedelta
from datetime import datetime

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
            context['shoes'] = Shoe.objects.filter(creator=request.user).filter(is_active=True)

            year, week, _ = now().isocalendar()
            month = now().month
            context['week'] = week

            last_week = now() - timedelta(weeks = 1)
            context['last_week'] = last_week.isocalendar().week

            month_obj = datetime.strptime(str(month), '%m')
            context['month'] = month_obj.strftime('%B')
            context['year'] = year

            context['weekly'] = Activity.objects.filter(created__year=year, created__week=week).order_by('-created')
            weekly_stats = generate_stats('weekly', context['weekly'])
            context = context | weekly_stats

            context['monthly'] = Activity.objects.filter(created__year=year, created__month=month).order_by('-created')
            monthly_stats = generate_stats('monthly', context['monthly'])
            context = context | monthly_stats
            context['activities'] = context['monthly']

            context['yearly'] = Activity.objects.filter(created__year=year).order_by('-created')
            yearly_stats = generate_stats('yearly', context['yearly'])
            context = context | yearly_stats

        return render(request, 'home.html', context)
