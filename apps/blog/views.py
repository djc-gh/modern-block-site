from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Comment, Reaction, Category, Newsletter
from .forms import PostForm, CommentForm
import json


class PostListView(ListView):
    """Display list of published posts with filtering and pagination"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(
            status='published',
            is_visible=True
        ).select_related(
            'author', 'category'
        ).annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True)),
            reaction_count=Count('reactions')
        ).order_by('-published_at')

        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(content__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(
            status='published', featured=True, is_visible=True
        ).select_related('author', 'category')[:3]
        context['categories'] = Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published', posts__is_visible=True))
        ).filter(post_count__gt=0)
        context['total_posts'] = Post.objects.filter(status='published', is_visible=True).count()
        return context


class PostDetailView(DetailView):
    """Display single post with comments and reactions"""
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published', is_visible=True).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Increment view count
        post.views_count += 1
        post.save(update_fields=['views_count'])

        # Get approved comments
        context['comments'] = post.comments.filter(
            is_approved=True
        ).select_related('author').order_by('-created_at')

        # Prepare reactions data for template
        reactions_data = [
            {'value': 'like', 'emoji': '👍'},
            {'value': 'love', 'emoji': '❤️'},
            {'value': 'happy', 'emoji': '😄'},
            {'value': 'wow', 'emoji': '😮'},
            {'value': 'sad', 'emoji': '😢'},
        ]
        context['reactions'] = reactions_data

        # Get user's reaction if logged in
        if self.request.user.is_authenticated:
            user_reaction = post.reactions.filter(user=self.request.user).first()
            context['user_reaction'] = user_reaction.reaction_type if user_reaction else None

        # Related posts
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            status='published',
            is_visible=True
        ).exclude(id=post.id).select_related('author')[:3]

        # Comment form
        context['comment_form'] = CommentForm()

        return context


class CategoryPostsView(ListView):
    """Display posts from specific category"""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category,
            status='published',
            is_visible=True
        ).select_related('author').order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class SearchPostsView(ListView):
    """Search posts"""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query),
            status='published',
            is_visible=True
        ).select_related('author', 'category').order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class AddReactionView(LoginRequiredMixin, View):
    """Add or update user reaction to post"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            reaction_type = data.get('reaction_type')

            post = get_object_or_404(Post, id=post_id)

            # Try to get existing reaction
            reaction, created = Reaction.objects.get_or_create(
                post=post,
                user=request.user,
                defaults={'reaction_type': reaction_type}
            )

            if not created:
                # Update existing reaction
                reaction.reaction_type = reaction_type
                reaction.save()

            # Get updated reaction counts
            reactions_count = post.reactions.values('reaction_type').annotate(
                count=Count('id')
            ).order_by('reaction_type')

            return JsonResponse({
                'success': True,
                'reactions': list(reactions_count),
                'user_reaction': reaction_type
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class AddCommentView(LoginRequiredMixin, View):
    """Add comment to post"""
    def post(self, request):
        try:
            form = CommentForm(request.POST)
            if form.is_valid():
                post_id = request.POST.get('post_id')
                post = get_object_or_404(Post, id=post_id)

                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                return JsonResponse({
                    'success': True,
                    'comment': {
                        'author': comment.author.get_full_name() or comment.author.username,
                        'content': comment.content,
                        'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p')
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class NewsletterSubscribeView(View):
    """Subscribe to newsletter"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )

            if not created and not newsletter.is_active:
                newsletter.is_active = True
                newsletter.save()

            return JsonResponse({
                'success': True,
                'message': 'Successfully subscribed to our newsletter!'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Admin Views
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to check if user is staff/admin"""
    def test_func(self):
        return self.request.user.is_staff


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """Admin dashboard"""
    template_name = 'blog/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.count()
        context['published_posts'] = Post.objects.filter(status='published').count()
        context['draft_posts'] = Post.objects.filter(status='draft').count()
        context['total_comments'] = Comment.objects.filter(is_approved=True).count()
        context['total_reactions'] = Reaction.objects.count()
        context['recent_posts'] = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
        context['recent_comments'] = Comment.objects.select_related('author', 'post').order_by('-created_at')[:5]
        return context


class AdminPostListView(AdminRequiredMixin, ListView):
    """Admin post list"""
    model = Post
    template_name = 'blog/admin/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.select_related('author', 'category').order_by('-created_at')


class AdminPostCreateView(AdminRequiredMixin, CreateView):
    """Create new post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/admin/post_form.html'
    success_url = reverse_lazy('blog:admin-post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdminPostUpdateView(AdminRequiredMixin, UpdateView):
    """Update post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/admin/post_form.html'
    success_url = reverse_lazy('blog:admin-post-list')


class AdminPostDeleteView(AdminRequiredMixin, DeleteView):
    """Delete post"""
    model = Post
    template_name = 'blog/admin/post_confirm_delete.html'
    success_url = reverse_lazy('blog:admin-post-list')
