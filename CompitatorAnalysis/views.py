from django.shortcuts import render

# Create your views here.
# myapp/views.py
import pandas as pd
import advertools as adv
import plotly.graph_objects as go
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

class SerpAnalyzeView(APIView):
    def post(self, request):
        query = request.data.get('query')
        gl = request.data.get('gl', 'us')

        if not all([query]):
            return Response({"error": "Query, search_engine_id, and search_engne_key are required parameters."}, status=400)

        serp_rankings = adv.serp_goog(q=[query], gl=[gl], cx='65ad0787cb9c54f76', key='AIzaSyAP-3UQVQdLpn5OvnZQiZy8ABruu3O1S-M')
        serp_rankings.to_csv('serp_heatmap.csv')

        return Response({"message": "SERP analysis completed and data saved."}, status=200)