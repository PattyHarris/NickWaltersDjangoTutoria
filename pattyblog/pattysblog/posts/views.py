from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def home(request):
    # Get all the post objects, ordered by the publishedDate
    # Return in a dictionary - the negative in the order by
    # sorts in reverse.
    posts = Post.objects.order_by("-publishedDate")
    return render(request, 'posts/home.html', {"posts": posts})


def post_details(request, post_id):
    # Show the details for the given post.
    # post = Post.objects.get(pk=post_id) - use the following instead
    # to generate a 404 on error:
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_details.html', {"post": post})
