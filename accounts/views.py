from django.views import View
from django.shortcuts import render

from activities.models import Location, Activity

class AccountsProfileView(View):
    def get(self, request):

        locations = Location.objects.filter(creator=request.user)
        activities = Activity.objects.filter(creator=request.user)
        
        context = {'locations': locations, 'activities': activities}
        return render(request, 'accounts-profile.html', context)
        
