from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})





class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/image_posts', default='', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='uncategorized')
    tag = models.CharField(max_length=100, default='#untagged', blank=True)

    def upload_image(self, filename):
        return 'post/{}/{}'.format(self.title, filename)

    def __str__(self):
        return f" title: {self.title}, author: {self.author}, category: {self.category}, tag: {self.tag}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.filter(active=True)
        return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments})

    def total_upvotes(self):
        return Post.objects.filter(pk=self.id).aggregate(Sum('votes__upvote'))

    def total_downvotes(self):
        return Post.objects.filter(pk=self.id).aggregate(Sum('votes__downvote'))

    @property
    def top_comments(self):
        return self.comments.filter(parent__isnull=True)

    @property
    def replies(self):
        replies = self.comments.filter(parent__isnull=False)
        #replies = self.comments.filter(parent_id=self.id)
        print(replies)
        return replies


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.post_id)])

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.body}, {self.name}, {self.id}, {self.parent}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    upvote = models.SmallIntegerField(default=0)
    downvote = models.SmallIntegerField(default=0)

    def get_all_objects(self):
        queryset = self.__class__.objects.all()
        return queryset

    class Meta:
        unique_together = (('user', 'post'),)

    def __str__(self):
        return f'Vote nr {self.id} cast by: {self.user} on post id: {self.post} up:{self.upvote} down:{self.downvote}'


