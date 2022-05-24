from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts-profile')
        context = {}
        return render(request, 'home.html', context)
        
