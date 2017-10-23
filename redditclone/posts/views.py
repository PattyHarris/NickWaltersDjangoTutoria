from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User


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
        post.save()

        # The hidden form passes to this view the next value which
        # is then used for redirection - that way, this works for both the
        # home and user_posts pages.

        if 'next' in request.POST:
            return redirect(request.POST['next'])

        return redirect('home')


# Decrement the number of votes for the post associated
# with the primary key
def downvote(request, primaryKey):
    if request.method == 'POST':
        post = Post.objects.get(pk=primaryKey)
        post.votesTotal -= 1
        post.save()

        # The hidden form passes to this view the next value which
        # is then used for redirection - that way, this works for both the
        # home and user_posts pages.

        if 'next' in request.POST:
            return redirect(request.POST['next'])

        return redirect('home')


# Challenge:
# Show the posts for the given author username.  I chose to filter by
# username here, and then send along the name and list of posts.
# The name really isn't needed since it's part of all the posts....
def user_posts(request, postAuthor):
    # Verify that this is a valid user since the URL may have been manually entered...
    try:
        user = User.objects.get(username=postAuthor)
        posts = Post.objects.filter(author__username=postAuthor).order_by('-votesTotal')
        return render(request, 'posts/user_posts.html', {"postAuthor": postAuthor, "posts": posts})

    except User.DoesNotExist:
        errorMessage = "Sorry, the user " + postAuthor + " is not in our database!'"
        return render(request, 'posts/user_posts.html', {"postAuthor": postAuthor, "error": errorMessage})
