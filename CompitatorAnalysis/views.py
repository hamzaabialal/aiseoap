from django.shortcuts import render

# Create your views here.
# myapp/views.py
import pandas as pd
import advertools as adv
import plotly.graph_objects as go
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from CompitatorAnalysis.serializers import SerpDataSerializer


class SerpAnalyzeView(APIView):
    def post(self, request):
        query = request.data.get('query')
        gl = request.data.get('gl', 'us')

        if not query:
            return Response({"error": "Query is a required parameter."}, status=400)

        serp_rankings = adv.serp_goog(q=[query], gl=[gl], cx='65ad0787cb9c54f76',
                                      key='AIzaSyAP-3UQVQdLpn5OvnZQiZy8ABruu3O1S-M')
        serp_rankings.to_csv('serp_heatmap.csv')
        keywords = serp_rankings["title"].tolist()

        serp_data = {
            'query': query,
            'gl': gl,
            'Keywords': keywords
        }
        serializer = SerpDataSerializer(data=serp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)