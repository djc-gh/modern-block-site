from django import forms
from .models import Post, Comment, Reaction

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'featured_image', 'category', 'status', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500', 'placeholder': 'Post Title'}),
            'excerpt': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500', 'rows': 3, 'placeholder': 'Brief summary'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500', 'rows': 10, 'placeholder': 'Full post content'}),
            'featured_image': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500'}),
            'status': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500'}),
            'featured': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-teal-500'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500',
                'rows': 4,
                'placeholder': 'Share your thoughts...'
            }),
        }
