from django.views import View
from django.shortcuts import render

class HomeView(View):
    def get(self, request):
        context = {}
        return render(request, 'home.html', context)
        
