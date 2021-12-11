from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, \
    PostDeleteView, UserPostListView, PostCommentView,  TagPostListView, \
    CategoryListView #SearchListView#PostVoteView,
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='gags-hot'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('tag/<str:tag>/', TagPostListView.as_view(), name='tag-posts'),
    path('about/', views.about, name='gags-about'),
    path('categories/<str:cat>', CategoryListView.as_view(), name='category-view'),
    path('search/', views.search, name='search-view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('hot/', PostListView.as_view(), name='gags-hot'),
    path('top/', views.top, name='gags-top'),
    path('post/<int:pk>/comment/', PostCommentView.as_view(template_name="gags/add_comment.html"), name='add_comment'),
    path('post/<int:pk>/upvote/', views.upvote, name='upvote'),
    path('post/<int:pk>/downvote/', views.downvote, name='downvote'),
]


#    path('post/<int:pk>/<str:slug>/', views.post_comment.as_view(), name='addcomment'),    path('post/<int:pk>/like/', views.like, name="like"),