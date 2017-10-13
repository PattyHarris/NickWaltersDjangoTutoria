from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.utils import timezone

# Create your views here.


@login_required
def create(request):
    if request.method == 'POST':
        # Should this be:
        #       if 'title' in request.POST?
        if request.POST['title'] and request.POST['url']:
            post = Post()
            post.title = request.POST['title']

            # The url needs a 'http://' or 'https://' - otherwise, the url is
            # becomes localhost:8000/www.blah.come
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                post.url = request.POST['url']
            else:
                post.url = 'http://' + request.POST['url']

            post.publishedDate = timezone.datetime.now()
            post.author = request.user
            post.save()
            # This needs to be a redirect, not render - otherwise, the path
            # in the browser shows /posts/create and not /posts/home.
            return redirect('home')
        else:
            return render(request, 'posts/create.html', {'error': 'Oops!  You must provide both a title and a URL to create a new Post.'})
    else:
        # Show the page
        return render(request, 'posts/create.html')


def home(request):
    # Get all the post objects sorted by the most votes first.
    posts = Post.objects.order_by('-votesTotal')
    return render(request, 'posts/home.html', {"posts": posts})


# Increment the number of votes for the post associated
# with the primary key
def upvote(request, primaryKey):
    # Get the object associated with the primary key - Nick uses pk as
    # the input variable name, but that makes the following function call
    # confusing... it's important to check for the method here - see the
    # Readme.md file regarding the odd error that can occur...

    if request.method == 'POST':
        post = Post.objects.get(pk=primaryKey)
        post.votesTotal += 1
        print(post.votesTotal)
        post.save()
        return redirect('home')


# Decrement the number of votes for the post associated
# with the primary key
def downvote(request, primaryKey):
    if request.method == 'POST':
        post = Post.objects.get(pk=primaryKey)
        post.votesTotal -= 1
        post.save()
        return redirect('home')
