from django.urls import path

from .views import (
    AdListView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView,
    CategoryListView, CategoryCreateView, CategoryDeleteView,
    AdImageView,
)


urlpatterns = [
    path('ads/', AdListView.as_view(), name='ads'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ads/<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('ads/<int:pk>/image/', AdImageView.as_view(), name='ad_image_upload'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]
