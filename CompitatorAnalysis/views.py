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
        url = request.data.get("url")
        gl = request.data.get('gl', 'us')

        if not query:
            return Response({"error": "Query is a required parameter."}, status=400)

        # Assuming adv.serp_goog() returns a DataFrame
        serp_rankings = adv.serp_goog(q=[query, url], gl=[gl], cx='65ad0787cb9c54f76',
                                      key='AIzaSyAP-3UQVQdLpn5OvnZQiZy8ABruu3O1S-M')
        serp_rankings.to_csv('serp_heatmap.csv')

        keywords = serp_rankings["title"].tolist()
        rank = serp_rankings["rank"].tolist()
        search_term = serp_rankings["searchTerms"].tolist()
        link = serp_rankings["link"].tolist()

        serp_data_list = []
        for i in range(len(keywords)):
            serp_data = {
                'query': query,
                'gl': gl,
                'user': self.request.user.id,
                'Keywords': keywords[i],
                'rank': rank[i],
                'search_term': search_term[i],
                'link': link[i],
            }
            serializer = SerpDataSerializer(data=serp_data)
            if serializer.is_valid():
                serializer.save()
                serp_data_list.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        return Response(serp_data_list, status=201)