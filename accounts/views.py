from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect

class AccountsProfileView(LoginRequiredMixin, View):
    ''' Redirects the user to the homepage after logging in.
    '''
    login_url = '/'
    redirect_field_name = 'next'

    def get(self, request):
        return redirect('home')
