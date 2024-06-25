from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Aiseoapp import settings
from groq import Groq
from rest_framework.generics import RetrieveAPIView, ListAPIView
from blogmanagement.models import Blogs
from blogmanagement.serializers import BlogsSerializer


# Create your views here.
class CreateBlogPost(APIView):
    def post(self, request, *args, **kwargs):
        topic = request.data.get('topic')

        user_input =  f"Please Write the Blog Article With headings of h2 , h3, and h4, and length of 5000 words On Which is Fully Plagirism Free: {topic}"

        if not user_input:
            return Response({"error": "Topic is required"}, status=status.HTTP_400_BAD_REQUEST)

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
            Blogs.objects.create(blog_title=topic, blog_content=response_content, user=request.user)
            return Response({"response": response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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