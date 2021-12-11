from .models import Comment, Post, Category
from django import forms

choices = Category.objects.all().values_list('name', 'name') #[('programming_humor', 'programming_humor'),('derpy_pets', 'derpy_pets'),('silly_vanilly', 'silly_vanilly'),('general_lulz', 'general_lulz'),('4_keks', '4_keks')]


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

