from django.views import View
from django.shortcuts import render

class AccountsProfileView(View):
    def get(self, request):
        context = {}
        return render(request, 'accounts-profile.html', context)
        
