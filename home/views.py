from django.views import View
from django.shortcuts import render

from activities.models import Location, Activity

class HomeView(View):
    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            context['locations'] = Location.objects.filter(creator=request.user)
            context['activities'] = Activity.objects.filter(creator=request.user)

        return render(request, 'home.html', context)
