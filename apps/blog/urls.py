from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Public views
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category-posts'),
    path('search/', views.SearchPostsView.as_view(), name='search-posts'),
    
    # API endpoints for reactions and comments
    path('api/reaction/', views.AddReactionView.as_view(), name='add-reaction'),
    path('api/comment/', views.AddCommentView.as_view(), name='add-comment'),
    path('api/newsletter/', views.NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    
    # Admin dashboard
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/posts/', views.AdminPostListView.as_view(), name='admin-post-list'),
    path('admin/posts/create/', views.AdminPostCreateView.as_view(), name='admin-post-create'),
    path('admin/posts/<int:pk>/edit/', views.AdminPostUpdateView.as_view(), name='admin-post-edit'),
    path('admin/posts/<int:pk>/delete/', views.AdminPostDeleteView.as_view(), name='admin-post-delete'),
]
