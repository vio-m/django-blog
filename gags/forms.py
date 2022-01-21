from .models import Comment, Post, Category
from django import forms

choices = Category.objects.all().values_list('name', 'name')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body', 'parent')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'category', 'tag')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(),
            'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }

