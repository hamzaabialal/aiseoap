
from django.urls import path, include
from . import views

urlpatterns = [
path('blog_create/', views.CreateBlogPost.as_view() ,  name='blog_creating'),
path('optimize_blog/', views.OptimzeBlogPost.as_view(), name='optimize_blog'),
    path('blog_list/<int:user_id>/' , views.UserBlogs.as_view(), name="blog_list"),
    path('blogpage/', views.BlogManagementPage.as_view(), name="blog_page"),
]

