import json

from groq import Groq
import advertools as adv
from Aiseoapp import settings
from CompitatorAnalysis.models import SerpResult
from keywordanalysis.models import KeywordResearch
from keywordanalysis.serializers import KeywordResearchSerializer
from management.models import StoreManagement
from shopifyproducts.models import Products
from shopifyproducts.serializers import ProductsSerializer
import requests
from rest_framework.generics import ListAPIView
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FetchProductDescription(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Products.objects.filter(user=request.user).values('description')
        return Response(list(queryset), status=status.HTTP_200_OK)

class KeywordSeoScoreView(APIView):
    def post(self, request, *args, **kwargs):
        # Fetch descriptions from Products model
        descriptions = Products.objects.filter(user=request.user).values_list('description', flat=True)
        description_text = " ".join(descriptions[0:10])

        user_input =  f"Please extract the relevant keywords from the following descriptions: {description_text} Provide the SEO scores, Your Output is Only in the form of a JSON response.:."

        if not user_input:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model="llama3-8b-8192",
            )
            response_content = chat_completion.choices[0].message.content
            return Response({"response": response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KeywordRankingView(APIView):
    def post(self, request, *args, **kwargs):
        # Fetch descriptions from Products model
        descriptions = Products.objects.filter(user=request.user).values_list('description', flat=True)
        description_text = " ".join(descriptions[0:10])

        user_input =  f"You Are keyword extractor bot Extract relevant keywords from the following descriptions: {description_text}.  E.g, If I need a tool named \"Keyword\"'s return value as an argument of \"keywords\", then the arguments array for \"keywords\" would look something like this considering:  {{keyword: \"name\", ranking:, 2]}} Your output should also be an array of these objects, each one having a name of the tool, the arguments to pass to it and the invocationHashm Include the enclosing markdown codeblock \\\`json\\\`"

        if not user_input:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model="llama3-8b-8192",
            )
            response_content = chat_completion.choices[0].message.content
            return Response({"response": response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckPlagiarism(APIView):
    def post(self, request, *args, **kwargs):
            # Fetch descriptions from Products model
            content = request.data.get("content")
            user_input = f"Please check the plagiarism of the following content: {content}."
            if not user_input:
                return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                client = Groq(api_key=settings.GROQ_API_KEY)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="llama3-8b-8192",
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stop=None,
                )
                response_content = chat_completion.choices[0].message.content
                return Response({"response": response_content}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckPlagiarism(APIView):
    def post(self, request, *args, **kwargs):
            # Fetch descriptions from Products model
            content = request.data.get("content")
            user_input = f"Please check the plagiarism of the following content: {content}."
            if not user_input:
                return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                client = Groq(api_key=settings.GROQ_API_KEY)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="llama3-8b-8192",
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stop=None,
                )
                response_content = chat_completion.choices[0].message.content
                return Response({"response": response_content}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KeywordsOptimization(APIView):
    def post(self, request, *args, **kwargs):
        # Fetch descriptions from Products model
        keywords = request.data.get("keywords")
        user_input = f"Please optimize the following keywords for better performance: {keywords}."
        if not user_input:
            return Response({"error": "Keywords are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model="llama3-8b-8192",
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stop=None,
            )
            response_content = chat_completion.choices[0].message.content
            return Response({"response": response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KeywordResearchView(APIView):
    def post(self, request):
        keyword = request.data.get("keyword")
        gl = request.data.get('gl', 'us')
        compitators = SerpResult.objects.filter(query__contains=keyword).last()
        compatitor_keyword = compitators.Keywords
        if not keyword:
            return Response({"error": "keyword is a required parameter."}, status=400)

        serp_rankings = adv.serp_goog(q=compatitor_keyword, gl=[gl], cx='65ad0787cb9c54f76',
                                      key='AIzaSyAP-3UQVQdLpn5OvnZQiZy8ABruu3O1S-M')
        serp_rankings.to_csv('serp_heatmap.csv')
        new_keywords = serp_rankings["title"].tolist()

        serp_data = {
            'user': request.user.pk,
            'compatitor_keywords': compatitor_keyword,
            'gl': gl,
            'Keywords': new_keywords
        }
        serializer = KeywordResearchSerializer(data=serp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ReteriveKeywordResearch(ListAPIView):
    serializer_class = KeywordResearchSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        queryset = KeywordResearch.objects.filter(user=user_id)
        return queryset

