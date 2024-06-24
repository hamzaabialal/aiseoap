from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard-2.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
