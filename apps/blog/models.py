from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Q
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#54C4C7', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, help_text='Brief summary of the post')
    featured_image = models.ImageField(upload_to='posts/%Y/%m/%d/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_visible = models.BooleanField(default=True, help_text='Show or hide this post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_publish_at = models.DateTimeField(null=True, blank=True, help_text='Schedule this post to go live at specific date and time')
    
    views_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False, help_text='Show this post on featured section')

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        """Estimate reading time in minutes"""
        word_count = len(self.content.split())
        return max(1, word_count // 200)

    @property
    def total_reactions(self):
        return self.reactions.count()

    @property
    def total_comments(self):
        return self.comments.filter(is_approved=True).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('happy', '😄 Happy'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'user']),
            models.Index(fields=['post', 'reaction_type']),
        ]

    def __str__(self):
        return f'{self.user.username} {self.reaction_type} {self.post.title}'


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
