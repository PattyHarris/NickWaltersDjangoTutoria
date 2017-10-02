# Blog Project

## Using Virtual Environments

    1. Install virtualenv (which I had already done for python).  Then, in the
    project folder, create the virtual folder - virtualenv vevn

    2. I had to use the following to make sure the virtual folder was created
    using python3:
        virtualenv --python=$(which python3) venv

    3. Activate the virtual environment:
        > source venv/bin/activate

        To deactivate:
        > deactivate

    4. Install django for the virtual environment -
    (venv) blahblahblah $  pip3 install django

    5. To see what's installed for the virtual environment:
    $ pip3 freeze

    6. With the virtual environment activated:
        > django-admin startproject <project name>

## Django App

    1. Every django project is supposed to have an "app" - the Pig Latin
    project didn't have an app.  The apps allow for modularization of the app
    code for a website.   This blog project really needs only a single app which
    will be for the posts.   But the challenge at the end of this tutorial will
    have us creating a "sitepages" app that will include all the pages such as
    about, navigation, etc.

    2. At the same level as manage.py
        > python3 manage.py startapp posts

        The files that we'll use this time are in the newly created posts
        folder.

## App Views

    1. To test the app at this point, again run
        > python3 manage.py runserver

        And then test again from the web browser at localhost:8000

    2. We need to point the urls to the views.py

        a. Add a templates folder under posts - here its really important
        that the folder is named "templates".  Add an additional folder using the
        app name, again in this case "posts". To this folder add a home.html
        page.

        b. Add the home function to posts/views.py - note that we need
        to use posts/home.html, not just home.html.

        c. And then, in urls.py,

            from posts import views
            .......
            url(r'^$', views.home)
            ........

        3. Lastly, to settings.py, add "posts" to the list of INSTALLED_APPS.

## Models

    1. Models, django, represent something we're trying to show on the website.
    Here, we're showing blog posts.  Each one has
        - a title
        - data
        - picture
        - text

        The model will be stored in the database.

        Since we're using images:
            > pip3 install pillow

    2. In models.py, add a class - note that the class name should
    be singular (e.g. Post not Posts) and start with a capital letter.

    3. (search for django model fields to get the doc for model attributes.
        See field types in the documentation.

    4. Before continuing with database setup, take care of any needed
    migrations - these are noted in the terminal window.
    > python3 manage.py migrate

    5. To add the model to the database, we need to make a migration for it.
    We initially commented it out when doing #4 above, but then to make a
    migration, uncomment the model code.  The first thing puts a file, in
    this case, 0001_initial.py, in the migrations folder.

        > python3 manage.py makemigrations
        > python3 manage.py migrate

        This is check for any new models that need to be added to the database.
        You then need to run migrate

        Any changes made to the model will be updated in the database the
        next time you run makemigrations.

## Django Admin Interface

    1. Create a super user:
        > python3 manage.py createsuperuser

    2. Login to the admin interface: localhost:8000/admin using the
    credentials setup above.

    3. To enable editing of Posts from the admin console, in admin.py
        from .models import Post
        .....
        admin.site.register(Post)
        ......

        This will then enable the Post model to show up on the console.
        From here you can add, delete, and modify data.

    4. Every post is labeled "Post Object".  By changing the Post model, we can
    provide the object label using the special function __str__(self) - see
    the model code.  To make these types of changes doesn't require
    the model to be update.  Just update the web page...

    5. For security, Nick recommends that you change the 'admin' url to
    something else - e.g. localhost:8000/<my unique admin web page name>
    and make the password really long, like "I eat cherios for breakfast"

## Making the Post Appear on the Web page

    1. The in views.py, get all the posts in the home function, sorted by the
    publishedDate - you can sort by any of the attributes defined.

    2. In home.html, cycle through all the posts using {% %} and {% endfor %}
    Nick indicates that this is not exactly python code - but is django python,
    according to some googling...

    3. A "pretty date" function is added to the model to create a formatted date.
    See publishedDatePretty().

    4. A "summary" function is added to the model to return only the first 100
    characters of the body.  See bodySummary()

## Working with images

    1. Images won't appear since the url given in the data points to
    some /media/blah area.  So we need to set where to find the data.
    To test the broken code, add <img src="{{ post.image.url }}"> to
    home.html and examine the html source - right click and select
    "Inspect Element".  Without the changes below, the path for the images
    is "media/DadsDahlia.JPG", which if you try to lookup using

        localhost:8000/media/blah

        doesn't show anything.  So the changes are needed below....

    2.  To fix,  in urls.py,  add the following:
            from django.conf.urls.static import static
            from django.conf import settings

        The static import is what will help server images.  The settings
        import just enables access to the settings file.

        Then to the urlpatterns, add the following:
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        In settings.py, add the MEDIA_URL and MEDIA_ROOT assignments to the
        end of the settings file.

## Regex

    1. We need to be able to create a url such that we can differentiate between
    posts once we've have them on the posts page - e.g. we should be able to use
    a url such as
        localhost:8000/posts/1

        to show the post associated with id=1

    You can test the post IDs by outputting {{ post.id }}

    2. The regex for the url needs /post/ + some number.

        url(r'^posts/(?P<post_id>[0-9]+)/$'), views.post_details)

        The ?P says I want to take the next part and turn it into a variable.
        So <post_id> is treated as a variable.  Here "post_id" is the name of
        the variable - it can be anything, e.g. my_post_id.  Then, the [0-9] says
        that anything that follows that is a number will be put into the
        variable.  The "+" says it can of any length.  The variable is then
        passed to views.py.

        The variable is then passed into the function in views.py - see
            def post_details(request, post_id)

## Post Details

    1. Get data from the database is as simple as (where pk is the primary key)
        post = Post.objects.get(pk=post_id)

        Then we pass "post" to the post_details function in views.py.

    2. Handling 404 - if the user decides to type in the url manually and puts
    in the wrong url (e.g. localhost:8000/posts/999), they'd get a call stack.
    To handle this, import get_object_or_404 from the shortcuts:
        post = get_object_or_404(Post, pk=post_id)

    With this, if you use localhost:8000/posts/999, you see a 404 page.

    3. Add an href from the home page on the title to link to the post details
    page.  With these, add a name to the url (e.g. post_details) in urls.py.

    4. Maybe see this about the orientation of images - they're wrong.
    https://stackoverflow.com/questions/12133612/using-pil-to-auto-rotate-picture-taken-with-cell-phone-and-accelorometer

## Bootstrap and Details

    1. From getbootstrap.com, copy the Basic Template and paste it into
    home.html.  The latest version is 4.0, but since the tutorial is using
    3.3,  I went back to that version (which is available on the website).
    The latest version has a Starter Template, which is very different...

    2. Copy also the bootstrap CSS - see Bootstrap CDN on the same
    page as the Basic Template.  Replace the "link" of the Basic Template.
    This change enables the web page to be served by bootstrap?

    3.  Copy the bootstrap javascript, again see the Bootstrap CDN.  Replace
    the javascript from the Basic Template.

    4. Replace the "hello world" in the Basic Template with the code we had
    before for the home.html.

## Boostrap Navigation Bar

    1. Under Components (on the bootstrap website), select the NavBar component
    on the right menu.  Copy the Brand html and paste it to the home.html under
    the <body> tag.  Remove the image tag line and change the href text to the
    blog name.  The # as an href says to to stay on the same page.

    "container-fluid" means the navigation bar will fill up the whole screen.
    This can be changed to just "container" which has a set size.

    2. To add the remaining navigation bar items, copy and paste from the example
    the code to add an un-ordered list to the home.html page above the end of
    the second  <div> tag:  Add the ending </ul> and </div>

    3. To the <ul>, add the <li> items, making sure each is inside a <a></a> -
    otherwise, they won't be clickable.

    4. The class="collapse navbar-collapse" makes it so when you resize the
    the browser, the navigation bar is resized appropriately - although the menu
    items may disappear.  To fix this add the html for the navbar collapse button
    which is a hamburger type button that appears on the right.  Add the
    html above the "brand" line.

    Nick removed the "Toggle Navigation" line.  And in the button tag, change the
    navbar-toggle collapsed to just navbar-toggle.  Also remove the aria-expanded.

    NOTE: the data-target value must be the same as the id in the next <div> tag.
    The default is bs-example-navbar-collapse-1, but you can change it to
    anything, as long as they match.  Nick changed it to mynav.

    This collapse code works only if you have the JS which is at the bottom of
    home.html.

    The lines in the hamburger menu are made with the "icon-bar" lines.

## Resizing Images

    1. First put the data related code (e.g. post.title) inside a div+container tag.

    2. In the img tag, add a class=img-responsive and a max-height style attribute.  Images are still rotated.

    3. Orientation issue: it's a problem with taking pictures on the iPhone.
    See https://stackoverflow.com/questions/17385574/stopping-auto-rotation-of-images-in-django-imagekit-thumbnail

    Fixed by rotating the images left, then right, and saving BEFORE uploading
    with django.

    4. To center the images, add center-block to the img-responsive class
    attribute.  This looks weird.

## Other Prettying

    1. Make the title h3

    2. Using the glyphicon-time from bootstrap.  Add a space and enclose in a
    h4 tag.

    3. Put the body in a <p> tag.

    4. Add a line under the "Latest Posts" heading - <hr/> tag.

    5. Center the welcome text with class=text-center

## Static Images

    1. Add a folder, "static" to the top level posts folder.  Add a posts folder
    inside the static folder (e.g. as we did with templates).

    2. Pull an image from unsplash.com - these are free.  I pulled this:
    Photo by Adarsh Kummur on Unsplash.  Move whatever image
    you're using into the folder created above.

    3. Add the img tag with the static image to home.html - code.  Before this
    tag you need to add {% load static %}

    4. Add the class and style attributes that we added for the individual post images, making this image a bit bigger.

## Cleanup

    1. There is a way to make the navbar and other container changes appear
    on every page, but for this part of the tutorial, we're going to copy the
    same stuff from the home.html the post_details.html.

    2. Copy everything from home.html and paste it to the top of post_details.
    The privious post_details stuff can actually be removed.

    3. Remove the Welcome and Latest Post titles as well as the dividing line.

    4. Remove the for-loop code.  Change post.summary to post.body and change the
    image height to about 300px.  Change the title from h3 to h1.

    5. Remove the Facebook menu item from both the home and post_details pages.

    6. Add the href for twitter to the twitter menu.

    7. Handle the "home" menu - add a href='{% url home %} ' to the
    blog title and add a "name" attribute to the home.html url in urls.py.  
    Add this href also to the home page's blog title as well.


    {{ }} - django variable
    {% %} - django "code"

## DISQUS

    1. From the website, you need to setup an account.

    2. For this tutorial, we are using the "install manually with
    Universal Code".  My blog is pattysblog.disqus.com - basic account
    (so there are ads).

    3. Copy the code DISQUS provides and paste at the end of the post_details
    page (but before the bootstrap js code)

    4. We need to add a PAGE_IDENTIFIER so that DISQUS can correctly
    identify the page.  If you don't provide this, DISQUS will use the URL
    of the page (which in this case is localhost).  You can also provide a
    PAGE_URL, but we're not doing this here.

    So, uncomment the commented out code and remove the line for the PAGE_URL.
    Change PAGE_IDENTIFIER to post-{{ post.id }}

    To prove that this works, hard-code post-1 in the code instead, and when you
    reload the page, the post for post-1 will appear (assuming you have added
    comment to that page).

## Challenge

    1. Create a new app which is sitepages.  This will hold the About and as well
    as Contacts (for example).  

    2. As an aid, change urls.py such that instead of importing (since it we're
    going to need to import from our new app - lessen confusion)
        from posts import views
    change this to
        import post.views

    Then change the urls to post.views.home and post.views.post_details

    Then, you would add:
        import sitepages.views

    and annotate the About page accordingly.

    3. Create the app (from these notes):
        > python3 manage.py startapp, sitepages

    4.   We need to point the urls to the views.py

        a. Add a templates folder under sitepages - here its really important
        that the folder is named "templates".  Add an additional folder using the
        app name, again in this case "sitepages". To this folder add a about.html
        page.

        b. Add the "about" function to sitepages/views.py - note that we need
        to use sitepages/about.html, not just about.html.

        c. And then, in urls.py,

            import sitepages.views
            .......
            url(r'^$', sitepages.views.about, name='about')
            ........

    5. Lastly, to settings.py, add "sitepages" to the list of INSTALLED_APPS.

## Vultr --> Digital Ocean

    1. Nick has an arrangement with Vultr such that we get free usage and he
    gets some $$ for that - anyway, reviews don't seem to be that great for
    the service.  No matter.  Get Nick's free credit from zappycode.com/Vultr

    2. There should have been free credit for $20 - didn't see it.  No matter, I paid $5 and will cancel after completion of this class.

    3. Once you're signed up, click on Servers on the left.  Pick the server
    type, in this case the Cloud (VC2), location (I picked Silcon Valley),
    server type (Ubuntu, version 16.04 x64), Server Size (25 GB/month) -
    the cheaper server was "sold out".  I am assuming when Nick did the class, the
    pricing was different.

    Add a Server Host Name and Label.  The other options can be skipped.
    Click "Deploy Now".

    4. Checking the Questions - Nick indicated the $20 was no longer valid and
    suggested using Digital Ocean - free credit of $10.  So, similar setup and
    server installed.  

    5. To access the server, use ssh from the terminal:
        > ssh root@<your IP>

    You initially need to use the password they send you, but then
    it will ask you to change it.  Using their console was impossible.
    The terminal is easier.

## Security on the Server

    1. Nick goes through changing the root password, which I already had to do:
        > passwd

    2. Then add a new user - django with a password.
        > adduser django

    3. Give the django user sudo rights:
        >usermod -aG sudo django

    4. Test (use CMD + t to open a new terminal tab) - leaving the latter
    terminal window open:
        > ssh django@<your IP>

    5. To prevent root logging in (not safe for root to have login privileges) -
    from the root terminal:
        > nano /etc/ssh/sshd_config

    Use the arrow keys to scroll down to "PermitRootLogin yes" - change to
    "no".   Use CTRL+x and "y" to save and exit.

    You then need to reload sshd -
        > systemctl reload sshd

    6. Exit from the root terminal and go back to the django user terminal.

    7. Firewall setup
        > sudo ufw app list

    It should come back with OpenSSH.

        > sudo ufw allow OpenSSH
            Rules updated
            Rules updated (v6)
        > sudo ufw enable
            Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
            Firewall is active and enabled on system startup
        > sudo ufw status
            Status: active
            To                         Action      From
            --                         ------           ----
            OpenSSH             ALLOW   Anywhere                  
            OpenSSH (v6)    ALLOW    Anywhere (v6)             

## Pip and Virtualenv

    1. Go to zappycode.com/djangoguide
        This takes you to a Digital Ocean's guide on how to setup Django on
        Ubuntu 16.04 - see
        https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

        We won't be setting up a PostgresSQL server.

    2. Make sure the server doesn't need updates, followed by upgrades
        > sudo apt-get update
        > sudo apt-get upgrade

    3. Make sure python3 is installed:
        > python3
        >>>exit()

    4. From the Django guide,
        > sudo apt-get install python3-pip
        > sudo apt-get install nginx
        > sudo pip3 install virtualenv

    5. We're going to use Gunicorn to run our website.  Then when someone
    hits our website, nginx will connect them to our website.  See more of this
    later.

## Getting the code on the server

    1. Install FileZilla (make sure to hit "no" on the menu changes and iDoctor)

    2. Host: use the IP address, in this case the IP Digital Ocean supplied for
    pattysblog:
       Username: django
       Password:
       Port: 22
       Click Quick Connect.

    3. You're not going to upload the venv, just the folder that's at the same
    level, e.g. pattysblog/pattysblog

    4. cd into pattysblog, and setup the virtualenv:
        > cd pattysblog
        > virtualenv venv
        > source venv/bin/activate

## Runserver on Digital Cloud

    1. We need to allow for port 8000:
        > sudo ufw allow 8000

    2. Install django and pillow (for images):
        > pip3 install django
        > pip3 install pillow

    3. To run the server, we need to specify 0.0.0.0 (otherwise, it will run localhost and we want it
        to be accessible to everyone.
        > python3 manage.py runserver 0.0.0.0:8000

    4. To test: <your IP>:8000
    This gives an error that we need to allow <your IP> in ALLOWED_HOSTS
    From FileZilla, find settings.py, right-click, and select "edit" - for me, it brings
    up a atom.io window.  Add the '<your IP>' to the ALLOWED_HOSTS array,
    and save (FileZilla will ask you if you want to upload the changes).

    Quit the server, and run again.

    4. The server indicated a reboot was required - see this article for handling:
    http://devanswers.co/system-restart-required-ubuntu-digitalocean-droplet/

## Gunicorn and nginx

    1. Install gunicorn in the virtual environment, e.g.
        > ssh django@<your ip>
        > login to the server...
        > cd into the blog folder and activate the virtual environment.

        Then,
            > pip install gunicorn

        This is also written up in the Digital Ocean guide under "Create a
        Gunicorn systemd Service File".

    2. Gunicorn is like runserver, but in a production mode.  runserver is ok for
    debugging on your own computer, but obviously not so good for production
    since you'd have to keep the terminal window open!

    3. To test, from same level as manage.py, run
        > gunicorn --bind 0.0.0.0:8000 pattysblog.wsgi:application

        And test from the browser using http://<your IP>:8000.
        The static image isn't showing on the home page, but that will be fixed
        later.

## Gunicorn systemd Service File

    1.  CTRL+C out of the running server and deactivate the virtual
    environment.

    2. From the Digital Ocean tutorial, create the new file:
    > sudo nano /etc/systemd/system/gunicorn.service

    3. Copy and paste from the same page the contents - after pasting, again,
    use CTRL+x to exit the editting, Y and "enter" to exit nano.

        [Unit]
        Description=gunicorn daemon
        After=network.target

        [Service]
        User=sammy
        Group=www-data
        WorkingDirectory=/home/sammy/myproject
        ExecStart=/home/sammy/myproject/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/sammy/myproject/myproject.sock myproject.wsgi:application

        [Install]
        WantedBy=multi-user.target

    4. Edit the above using FileZilla - much easier....
    Open up the /etc/systemd/system/gunicorn.service
    file.  Unfortunately, it requires "sudo" so we ended up deleting the contents
    of the file and pasting in the changes....

    5. Start the service:
        > sudo systemctl start gunicorn
        > sudo systemctl enable gunicorn

    As indicated in the online documentation, if you make changes to the service:
        > sudo systemclt daemon-reload
        > sudo systemctl restart gunicorn

## Configure Nginx

    1. Create a new server block in Nginx's sites-available directory - I have no idea
    what this is about.
        > sudo nano /etc/nginx/sites-available/pattysblog

        And using the Digital Ocean documentation, copy and edit the following:
            server {
                listen 80;
                server_name <your domain IP>;

                location = /favicon.ico { access_log off; log_not_found off; }
                location /static/ {
                    root /home/django/pattysblog;
                }

                location / {
                    include proxy_params;
                    proxy_pass http://unix:/home/django/pattysblog/pattysblog.sock;
                }
            }

    2. This creates a symlink....test with the second line.  Lastly, restart nginx
        > sudo ln -s /etc/nginx/sites-available/pattysblog /etc/nginx/sites-enabled
        > sudo nginx -t
        > sudo systemctl restart nginx

    3. Cleanup the firewall stuff we created before - from the documentation: "Finally,
    we need to open up our firewall to normal traffic on port 80. Since we no longer
    need access to the development server, we can remove the rule to open port
    8000 as well:"
        > sudo ufw delete allow 8000
        > sudo ufw allow 'Nginx Full'


    4. Static image - at this point, you can use just the IP for the domain without
    the port 8000 and it all works, except for the static image.  To fix, open
    settings.py from FileZilla.  Add to the place where we also have STATIC_URL
    defined:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

    5. Collect all the static files - this has to be done in venv - see the Q&A.
        > python3 manage.py collectstatic

        With above changes, the static image now appears.

    6. Nick then registered the IP with his domain using Google.   For any domain where
    you are registered, you need add a host record with the IP of the our blog website.
    Nick uses nickwalters.info and then adds the host record.

    7. Additional changes - first to Nginx and then second to settings.py.
        > sudo nano /etc/nginx/sites-available/pattysblog

        Here, we need to change this line to add where the IP is located:

                server_name <your IP> <your domain>;
            e.g.
                server_name 45.32.206.238 nickwalters.info;

        And then restart Nginx:
            > sudo systemctl restart nginx

        Then in settings.py, add nickwalter.info to ALLOWED_HOSTS

            ALLOWED_HOSTS = ['45.32.206.238', 'nickwalters.info']

        And then restart gunicorn:
            > sudo systemctl restart gunicorn
