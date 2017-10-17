# Redit Clone Project

    The emphasis of this project is to handle user authentication.

## Project Setup

    1. Start the django project:
        > django-admin startproject redditclone

    2. Setup the virtual environment - make sure you're at the same level as manage.py
        > virtualenv --python=$(which python3) venv
        > source venv/bin/activate

    3. Install django and test:
        > pip3 install django
        > python3 manage.py runserver

        And then go to a web browser with localhost:8000

    4. Exit runserver (ctrl+c) and migrate any changes:
        > python3 manage.py migrate

    5. If you look at settings.py, you'll see that an auth package comes
    standard with the default setup.  

    6. Create the super user:
        > python3 manage.py createsuperuser

    7. Create the accounts app
        > python3 manage.py startapp accounts

    8. urls.py changes
        .....
        import accounts.views
        .....

        url(r'^signup/', accounts.views.signup)

    9. Create the templates folder and signup page (note that if you specify a folder
        that doesn't exist in atom, it will create the folder for you).  Add something
        the page (e.g. Hello!)

    10. In views.py add the test function (for now):

        def signup(request):
            return render(request, 'accounts/signup.html')

    11. Add the accounts app to the settings.py.  At this point, you should be able
    to type localhost:8000/signup in a browser and see the Hello (or whatever)

## Signup Form

    1. Setup the form with the action="signup" - that tells the form "where to go".
    Along with this change, add name="signup" to the urls.py:
            <form action="{% url 'signup' %}" >
            ......
            url(r'^signup/', accounts.views.signup, name='signup')
            .......

    2. Change the form method to POST - this also makes it so the submitted
    parameters don't appear on the submitted url.  We also needed to add
        {% csrf_token %}
    which is cross site forgery protection.

    3.  The signup.html page handles both the GET and the POST.  The GET request
    comes in when the user clicks on the page to sign up.  The POST request
    comes in when the user clicks "submit" - recall that the form method=POST.
    When the request is a POST, we'll create the user given the information entered.

    4. Later we will be using the documentation from the Django website - see Django
    Athentication, Working with User Objects

## Creating User Objects

    1. Beginning with the Django documentation above, in the section of Creating Users,
    add the following import:
        from django.contrib.auth.models import User

    2. To create a user, use the User.objects.create_user method as described in the
    documentation.  Note the primary attributes we need to use: username, password,
    email, first_name, last_name
        e.g.
            User.objects.create_user(request.POST['username'],
                password=request.POST['password1']

### Unique User Names

    1. Check to see if the name already exists by searching the data for the given name.
    Here we make use of a try/except.  

### Login User after Signup

    1. If the user is created, login that user.  This also required an addition
    import - this is all in the Django documentation as well.

    2. To test, add a new user (which is then logged in) and then go to the admin
    page - you'll get an error since this new user doesn't have admin privileges.

## Login User Page

    1. Copy the signup.html page and rename to login.html (this new page is nearly
        identical to the signup page).  The changes are minimal, UI-wise.

    2. Go to the Django documentation "How to log a user in" - this is where you need
    the 'authentication' import.

    3. The function name "login" is also part of the Django framework, causing a runtime
    error (software is confused) - so the view.py function of "login" was changed to
    "loginView".

## URL Includes

    1. To add the include, we need to also add the following import to
    urls.py:
        from django.conf.urls import Includes

    Then, we need to add the following URL - here we have the name of our app,
    'accounts' plus the urls.py file (which is added next):
        url(r'^accounts/', include('accounts.urls')),

    2. Add a urls.py file to the accounts app structure and initially copy and paste
    the contents from the redditclone/urls.py file to this new file and edit to only
    include the signup and login urls.  The redditclone/urls.py is edited as well to
    eliminate the signup and login urls.

    3. To test, use localhost:8000/accounts/login/
    NOTE: At this point, we need to specify "accounts" as part of the path.

    4. Another improvement to this structure is to add an app_name which is then
    used in the templates to specify the appropriate view - this is becomes more
    critical with numerous apps and their views.  In accounts/urls.py, add
        app_name = 'accounts'

    Then, in both login.html and signup.html, the app_name needs to be added to the
    view:
        e.g.
            <form  method="POST" action="{% url 'accounts:signup' %}">

    NOTE: it's app_name + colon, not app_name + dot

## Post App

    1. Create the posts app - e.g. CTRL+c out of the server and run
        >python3 manage.py startapp posts

    Add the posts app to settings.py

    2. The new view is "create" -
        - add template/posts/create.html
        - edit posts/urls.py to include the new create url
        - include the posts/urls in redditclone/urls

    3. To test, add a temporary create function to post/views.py to return
    the create.html page - add some text to the latter (e.g. Hello).  Don't forget to
    start the server again - python3 manage.py runserver

    3. We only want to allow users who have logged in to create posts.  In the Django
    documentation, see search for "login_required" - see the section "Limiting access
    to logged-in users" and the "login_required decorator".  Basically, you add the
    following above the view function:

        @login_required
        def create(request):
            ...

    See the documentation for details, but this works because we have setup an
    accounts/login.  If the user isn't logged in, the login_required redirects them to
    the login page.  You can also specify a different page - see the docs for details.

## Redirect Login

    1. Django attaches to the login url the page that redirected to the login page, in
    this case, the create page -
    .../accounts/login/?next=/posts/create

    2. In the login.html form, add the following code to access the redirect:

        {% if request.GET.next %}
        <input type="hidden" name'"next" value={{ request.GET.next }}
        {%  endif %}

    And then if the login is successful, add the accounts/view.py add "redirect" to the
    shortcuts import and add this logic to the successful login (loginView function):
        if 'next' in request.POST:
            return redirect(request.POST['next'])

    To test, force the user to be redirected to the login page (e.g. user is not logged
    in) and by inspecting the elements on the page, you'll see the hidden field.
    Note that here it's better to check if 'next' has anything as opposed to
    checking:
        if request.POST['next'] is not None:

## Posts Form

    1. Start with the login.html as a template and copy that to create.html.
    It's a simple form with a title, url, and a Post button.

## Post Model

    1. In posts/models.py, add the Post class with models.Model as input.
    "models.Model" means that the Post is a Django Model, so Django knows that it
    should be saved in the database.

    2. The author will be a foreign key to the user object that created the post.  That
    will allow searching on the author - e.g. how many posts has this author created.
    We need to import User - then author becomes
        author = models.ForeignKey(User)

    3. Run the migration - e.g. quit the server and
        > python3 manage.py makemigrations
        > python3 manage.py migrate

    If you look at the migration file, you'll see the foreign key setup for the
    author field.

## Saving a Post

    1. In the posts/views.py, the create function needs to handle both the
    request.POST and request.GET

    2. To get the logged in user, it's very simple - just request.user.

    3. posts/admin.py, we need to register the model - as we did with the blog tutorial.
    Now, if you check the admin page, you should see a post when it's saved.

    4. Every post is labeled "Post Object".  By changing the Post model, we can
    provide the object label using the special function __str__(self) - see
    the model code.  To make these types of changes doesn't require
    the model to be update.  Just update the web page...

    5. If the title or url is not provided, return a error as we did in accounts.
    The error is returned as a dictionary.  See the Django Girls tutorial on
    CSS to change the error to red and other prettying..

## Home Page - URL

    1. Normally the Home page would have it's usual Home page URL, but here
    Nick is trending towards the Home page being part of the posts.  Also, we
    were getting away from having explicit URLs in urls.py,  but it looks like the Home
    page will be an exception....

    2. In urls.py, add the import for the post.views - e.g.
        from posts import views

    And then add the following url:
        url(r'^$', views.home, name="home"),

    Then, in posts/views add this (temporary return):
        def home(request):
            return render(request, 'posts/home.html')

    3. If you call render instead of redirect, the path shown in the web browser
    stays as posts/create.  We want it to show posts/home - so we need a redirect.

## Home Page - HTML

    1. Basic HTML setup for the home page - add just enough HTML at this
    point to display the data.

    2. We need to check the given URL for http/https - if the user doesn't supply that
    the path becomes localhost:8000/www.google.com, which doesn't work.  If the
    user doesn't supply it, preface the url with http.

    3. To handle the up and down votes, upVote and downVote urls and methods are
    added to the posts/urls.py and posts/views.py - the regex here specifies the name
    'primaryKey'+any number - e.g. primary key plus a number.

        url(r^'(?P<primaryKey>[0-9]+)/upvote', views.upvote, name='upvote'),
        url(r^'(?P<primaryKey>[0-9]+)/downvote', views.downvote, name='downvote'),

    To test, you should be able to use localhost:8000/posts/1/upvote
    or whatever the ID of the post - localhost:8000/posts/<id>/upvote.

    4. The issue with the wrong counts (both for up and down vote totals) has to do
    with the way browsers handle what's typed in the URL bar - when you type in

        localhost:8000/posts/1/upvote

    without hitting return, Safari goes to check what's at that URL - which explains
    why the terminal showed this without hitting return:

        [09/Oct/2017 22:00:21] "GET /posts/4/upvote HTTP/1.1" 302 0
        [09/Oct/2017 22:00:21] "GET / HTTP/1.1" 200 358

    For both upvote and downvote, add the check for method = POST.

    5. In order for the up and down votes to work as a POST, we need to use a form -
    add the form to replace the current up and down href's.  Also send along the
    post.id field as part of the submit - instead of this:

        <a>UP</a> {{ post.votesTotal }} <a>DOWN</a>

    use this

    <form  method="POST" action="{% url 'posts:upvote'  post.id%}">
        {% csrf_token %}
        <input type="submit" value="UP">
    </form>
    {{ post.votesTotal }}
    .....
    And likewise a form for the downvote.

## Extending Templates

    1. Create a site wide template that can be used across the site's HTML
    pages.  Add a new folder at the project level with a file base.html -
        /redditclone/templates/base.html

    2. Add 'templates' to the TEMPLATES dictionary in redditclone/settings.py
        'DIRS': ['templates'],

    3. Basic setup is you create a html file like this - assume this is base.html (note
        the NAVBAR and FOOTER text is test text):
        NAVBAR!
        <br/>
        <br/>

        {% block content%}
        {% endblock %}
        <br/>
        <br/>
        FOOTER

    Then, in the html file that uses it, at the top of the page add:
        {% extends 'base.html' %}

        {% block content %}

        < html code goes here>

        {% endblock %}

    4. Add this basic template code to each view (e.g. create, home, signup, and login)
    Test with /<home>
                /posts/create
                /accounts/signup
                /accounts/login

## Verifying User is Logged In

    1. To get started with the navigation bar, copy and paste the entire contents of the
    pattysblog/posts/templats/posts/home.html and paste it to the top of
    base.html.    Remove everthing between
                <div class="container">
                </div>

    2. Move the block content HTML inside the div container - e,g,
            <div class="container">
                {% block content%}
                {% endblock %}
            </div>
    Remove the rest of the test NAVBAR and FOOTER code.

    3. For now, remove the url that points to the About page (since we don't have one
    yet).  You should be able to test the home page now and there should be a
    proper navigation bar.  At this point, change the 2 occurrences of Patty's Blog to
    Reddit Clone.

    4. To move the navigation menu items to the right, all you need to do is add
    "navbar-right" to the nav class item:
        <ul class="nav navbar-nav navbar-right">

    5. Add a check for whether the user is authenticated to determine whether the
    menus show "Logout" or "Login Signup".  Add the appropriate URL's to each
    menu item:
            <li><a href="{% url 'accounts:signup' %}">Signup</a></li>
            <li><a href="{% url 'accounts:login' %}">Login</a></li>

## Logout

    1. 3 Steps:
        1. Create the URL pattern (accounts)
        2. Create the code behind the view
        3. Connect the Logout menu to the URL

    2. GET or POST: There's a stackoverflow question on the subject - if you user
    a GET, you can run into issues (as we saw earlier).  So, we'll make logout
    a POST.  See https://stackoverflow.com/questions/3521290/logout-get-or-post

    3. In the Django documention, see "How to log a user out":
        logout(request)

    4. To make this a POST method, again from stackoverflow, we'll put a hidden form
    inside the navigation bar and access the form using the element ID.
    See https://stackoverflow.com/questions/12589739/posting-action-data-to-twitter-bootstrap-logout-button

    5. If the user logs out, we use a redirect the user to the home page.  Also at this
    point, after the user logs in, we can redirect them to the 'home' page as well.

## Tidying Up

    1. Add some space before the Signup button - I already had that.

    2. Make the button a bootstrap button - see the documentation (search Google for
    bootstrap button).  For the login, signup, and create pages, add to each button:
        class="btn btn-primary"

    3. We can also add the above class to the home page's "a" tag:

    4. Use a table to setup the 'home' pages buttons with the text on the side.
    First, temporarily move the upvote and downvote forms to the bottom of the page.

    5. Nick uses a single table - seems to work although tables within tables might be
    better.

    6. Add some padding between the columns with the style="padding-right: 20px;"

    7. Use the formatted post publishing date - publishedDatePretty.

    8. Find the up and down arrows from bootstrap glyphs - we used the triangle-top
    and triangle-bottom glyphs.  The code is provided by bootstrap:
        <span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>

    You just need to copy the text for the glyph you want to use and replace the
    search text in the span class provided (see above)

    9. To POST the up and down votes, we used the same "get element by ID" method that
    we used in base.html.   The forms must be inside the for-loop, since we need a form
    for each row in our table.  Also the forms must be made hidden (which they're
    weren't before).  Add the post.id to each of the form ID's since there will be a
    form for each row and it must be unique.  Right-click and select Inspect Element
    from the browser to see the results of these changes.

## Challenge

    1. On the home page, make the user's names clickable such that when clicked,
    redirects the user to a list of posts by that user.  The title of the page should
    be "Posts by <username>".  No New Post button is needed, but it will list all the
    posts by that user.

    2. Regex: https://stackoverflow.com/questions/32395062/django-urlpattern-for-username

    3. As part of looking into foreign keys, you can test in the shell by exiting the
    server and typing
        > python3 manage.py shell
        >>> from posts.models import Post
        >>> Post.objects.all()
        >>> Post.objects.filter(author__username='Able')

    4. I could have used the selected post's user object as a way to get all the
    posts for that user, but I wanted to be able to have the url be
        /posts/<username>

    This took some Googling for filter and then filtering with foreign keys.

    5. I also wanted to make re-use of the upvote and downvote views.  I made use of
    the hidden fields, passing in the "next" value in the form.  Still not sure this is
    the best way of doing this.   Alternatively, separate views and URLs could be used
    to handle the up and down arrows from the user posts template.

    6. 
