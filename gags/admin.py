from django.contrib import admin
from .models import Post, Comment, Vote, Category
from tinymce.widgets import TinyMCE
from django.db import models



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title and Author', {'fields': ['title', 'author']}),
        ("Content", {'fields': ['content']}),
        ("Categories and tags", {'fields': ['category', 'tag']})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user_id')
    list_filter = ('post_id', 'user_id')
    search_fields = ('post_id', 'user_id')
    actions = ['delete upvotes']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)





