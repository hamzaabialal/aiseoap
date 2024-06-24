
from django.urls import path
from . import views

urlpatterns = [
    path('compitatoranalysis/', views.SerpAnalyzeView.as_view(), name="compitator_analysis")
]
