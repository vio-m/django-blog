from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.db.models import Q
from .models import Post, Comment, Vote, Category
from .forms import CommentForm, PostForm
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Count


def hot(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'gags/hot.html', context)



class PostListView(ListView):
    model = Post
    template_name = 'gags/hot.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'gags/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "gags/add_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)







def upvote(request, pk):
    post_id = Post.objects.get(pk=pk)
    user_id = request.user.id
    try:
        voted = Vote.objects.get(post=post_id, user=user_id)
        return HttpResponse("YOU ALREADY VOTED")
    except:
        upvote_instance = Vote.objects.create(post_id=pk, user_id=user_id, upvote=1)
        upvote_instance.save()
        return redirect(post_id)

def downvote(request, pk):
    post_id = Post.objects.get(pk=pk)
    user_id = request.user.id
    try:
        voted = Vote.objects.get(post=post_id, user=user_id)
        return HttpResponse("YOU ALREADY VOTED")
    except:
        downvote_instance = Vote.objects.create(post_id=pk, user_id=user_id, downvote=1)
        downvote_instance.save()
        return redirect(post_id)


def about(request):
    return render(request, 'gags/about.html')


def top(request):
    ordered = Post.objects.annotate(upvote_count=Count('votes')).order_by('-upvote_count')
    context = {'posts': ordered}
    paginate_by = 3
    return render(request, 'gags/top.html', context)


class TagPostListView(ListView):
    model = Post
    template_name = 'gags/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return Post.objects.filter(tag=tag)


class CategoryListView(ListView):
    model = Post
    template_name = 'gags/categories.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        cat = self.kwargs.get('cat')
        return Post.objects.filter(category=cat)

def get_category(request):
    categories = Category.objects.all()
    context = {'category_list': categories}
    return render(request, 'gags/categories.html', context)

def search(request):
    qd = request.GET.get('q')    # This is a dictionary
    qs = Post.objects.all()      # This is a QuerySet
    if qd is not None and qd:       # WTF?
        lookups = Q(title__icontains=qd) | Q(content__icontains=qd)     # lookup is set to search in two columns: title and content
        qs = Post.objects.filter(lookups)
    context = {
        "results": qs
    }
    return render(request, 'gags/searched.html', context)






