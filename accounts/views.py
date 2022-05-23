from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from activities.models import Location, Activity

class AccountsProfileView(LoginRequiredMixin, View):
    ''' Profile view for a user.
    '''
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):

        locations = Location.objects.filter(creator=request.user)
        activities = Activity.objects.filter(creator=request.user)
        
        context = {'locations': locations, 'activities': activities}
        return render(request, 'accounts/accounts-profile.html', context)
        
