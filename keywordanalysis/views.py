import json

from groq import Groq

from Aiseoapp import settings
from management.models import StoreManagement
from shopifyproducts.models import Products
from shopifyproducts.serializers import ProductsSerializer
import requests
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
        description_text = " ".join(descriptions)

        user_input =  f"Please extract the relevant keywords from the following descriptions: {description_text} Provide the SEO scores in the form of a JSON response. Remove the phrase Here is the JSON response: from the output."

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
        description_text = " ".join(descriptions)

        user_input =  f"Please extract the relevant keywords from the following descriptions: {description_text} Provide the Google Ranking of These keywords in the form of a JSON response. Remove the phrase Here is the JSON response: from the output."

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



