import pandas as pd
import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from Aiseoapp import settings
from groq import Groq
from rest_framework.generics import RetrieveAPIView, ListAPIView
from blogmanagement.models import Blogs
from blogmanagement.serializers import BlogsSerializer
from management.models import StoreManagement
from shopifyproducts.models import ShopifyAccessToken


# Create your views here.
class CreateBlogPost(APIView):
    def post(self, request, *args, **kwargs):
        topic = request.data.get('blog_name')
        product = request.data.get('product')
        location = request.data.get('location')
        upload_csv = request.FILES.get('upload_csv')
        limit = int(request.data.get('limit', 0))
        access_token = ShopifyAccessToken.objects.get(user=request.user).access_token
        store = StoreManagement.objects.get(user=request.user)
        shopify_url = f"https://{store.store_name}.myshopify.com/admin/api/2021-07/articles.json"
        base_url = f"https://{store.store_name}.myshopify.com/"
        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        if upload_csv:
            try:
                upload_csv = pd.read_csv(upload_csv)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if not topic and upload_csv.empty:
                return Response({"error": "Either topic or upload_csv is required"}, status=status.HTTP_400_BAD_REQUEST)

            upload_csv = upload_csv["title"].tolist()

            published_urls = []
            for topic in upload_csv:
                user_input = f"Please Write the Blog Article With headings of h2 , h3, and h4, and length of 5000 words On Which is Fully Plagirism Free: {topic} and my featured product is {product} and Write blog for location {location}"
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
                    blog = Blogs.objects.create(blog_title=topic, blog_content=response_content, user=request.user)

                    # Upload the blog to Shopify and get the URL
                    blog_url = self.upload_to_shopify(blog, shopify_url, headers, store.store_name)
                    published_urls.append(blog_url)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"data": "Blogs have been published in the Shopify store", "urls": published_urls}, status=status.HTTP_200_OK)

        else:
            if not topic:
                return Response({"error": "Topic is required"}, status=status.HTTP_400_BAD_REQUEST)

            published_urls = []
            while limit > 0:
                user_input = f"Please Write the Blog Article With headings of h2 , h3, and h4, and length of 5000 words On Which is Fully Plagirism Free: {topic} and my featured product is {product} and Write blog for location {location}"
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
                    blog = Blogs.objects.create(blog_title=topic, blog_content=response_content, user=request.user)
                    limit -= 1

                    # Upload the blog to Shopify and get the URL
                    blog_url = self.upload_to_shopify(blog, shopify_url, headers, store.store_name)
                    published_urls.append(blog_url)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"data": "Blogs have been published", "urls": published_urls}, status=status.HTTP_200_OK)

    def upload_to_shopify(self, blog, shopify_url, headers, store_name):
        data = {
            "article": {
                "title": blog.blog_title,
                "body_html": blog.blog_content,
                "author": blog.user.username
            }
        }

        response = requests.post(shopify_url, headers=headers, json=data)

        if response.status_code != 201:
            raise Exception(f"Failed to upload blog to Shopify: {response.json()}")

        article = response.json()["article"]
        blog_id = article["blog_id"]
        article_handle = article["handle"]

        # Construct the public URL
        blog_url = f"https://{store_name}.myshopify.com/blogs/{blog_id}/articles/{article_handle}"
        return blog_url



class OptimzeBlogPost(APIView):
    def post(self, request, *args, **kwargs):
        blog = request.data.get('blog')

        user_input =  f"Please Optimize The Blog Post For Seo For Ranking Google , Bing and yahoo: {blog}"

        if not user_input:
            return Response({"error": "blog is required"}, status=status.HTTP_400_BAD_REQUEST)

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


class UserBlogs(ListAPIView):
    """API view to retrieve blogs for a specific user."""
    serializer_class = BlogsSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Blogs.objects.filter(user_id=user_id)


class BlogManagementPage(TemplateView):
    template_name = 'blog/product-edit.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
