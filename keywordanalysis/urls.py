
from . import  views
from django.urls import path, include

urlpatterns = [
    path('keyword_seo_analysis/', views.KeywordSeoScoreView.as_view(), name="seo_analysis"),
    path('check_plagiarism/', views.CheckPlagiarism.as_view(), name='check_plagiarism'),
    path('keyword_ranking/', views.KeywordRankingView.as_view(), name='keyword_ranking'),
    path('keywordoptimization/', views.KeywordsOptimization.as_view(), name='keyword'),
    path('product_discription/', views.FetchProductDescription.as_view(), name='product_discription'),
    path('keywordresearch/', views.KeywordResearchView.as_view(), name="keyword_research"),
    path('reterivekeywords/<int:user_id>/', views.ReteriveKeywordResearch.as_view(), name='reterive_keywords')
]
