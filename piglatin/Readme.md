# Python Notes

    1. First to see if python is installed,
        > python3 --version

        What we really need here is python3 - so that needs to be installed.
        Go to python.org - here you can easily download and install python3

        I had to use another article to setup atom for python -
        https://medium.com/@andrealmar/how-to-setup-atom-as-your-python-development-environment-a67fe8738bd3

        Turns out Nick uses atom.io too, so hopefully, all my changes work!

    2. Basic introduction to python syntax - see the code in pythonRefresher.py
        Nick goes over variables, strings, printing, comments, etc.
        Classes are a bit odd - you can add class instance variables on the fly.
        Also methods must have "self" as the first parameter
            e.g. def bark(self)
        BUT, the word "self" can really be anything else
            e.g. def bark(me)
        See the code example - especially the __init__ function.

# Django Notes

## Installation

    1. Simple.  
        > pip3 install Django

    2. To test the installation, in a terminal window

    > python3
    >>> import Django
    >>>print(django.get_version())
    1.11.5
    >>>exit()

## Creating a Project - Pig Latin

    1. A project, in this case piglatin, is started using the following command:
        > django-admin startproject piglatin

        This will create a folder called piglatin in the current directory.  It is common to make the project name all lowercase.

    2. To test, run the manage.py file using "runserver" as an input argument.
        > cd piglatin
        > pthyon3 manage.py runserver

        This gives you the location of your server which you can then paste into a
        web browser - e.g. http://127.0.0.1:8000/
        You can also use localhost:8000

## Contents of the Project folder

    1. The settings.py contains settings about the project - all top level settings/
    2. urls.py - traffic director for visitors to your site.  Tells where you'll send visitors based on the URL.  Manages traffic.
    3. wsgi.py - more top level settings - shouldn't need to be changed.  

    There's really not much you'll want to change with the default files.

### urls.py and Views

    1. The urlpatterns array holds the strings that route traffic.  On startup, it contains a single entry.  If you take the startup web page, localhost:8000 and change it to localhost:8000/admin you see a login for an admin web page.

    2. HelloWorld web page: add another entry to the urlpatters:
        url(r'^hello/', admin.site.urls),

        The r'blah' is regex.

        In django, when someone passes in a URL, you give them a view -
        create a file called views.py.  Here you create your webpage stuff, and
        then in urls.py you add the import and the entry into urlpatterns -

        from . import views

        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^hello/', views.hello)
        ]

        where views.hello represents the function defined in views.py.  The
        response can only send back a string - next up, the sending back an HTML
        page.

            def hello(request):
                return HttpResponse("Hello World!")

### HTML Pages

    1. Create a folder "templates" - this is standard for django.  The folder must reside at the same level as the manage.py file.

    2. Create a file to represent the first page - in this case, "home" - the page name should always represent the page.

    3. Edit the settings.py file - where it shows the "TEMPLATES dictionary  - to the "DIRS" array,  "templates".

    4. Then, back in views.py, import "render" - which helps to render HTML pages.
    Now, our hello function looks like this:
        def hello(request):
            return render(request, 'home.html')

    Further reading w3schools.com, HTML has more information on using HTML.

    4. To make this more legit, change the "hello" page to "home" (and likewise everything else "hello").  Then in urls, you only need this - note the "$"
            url(r'^$', views.home)

### Form Actions

    1. To add python to the form action, include the code between {%  %}
        e.g. <form action="{% %}" />

        With that, provide a name for the url we're going to, in this case, call it "translate" - this can be anything.  In urls.py, add a "name=" parameter to the translate url:
            url(r'^translate/', views.translate, name='translate')

        Likewise, we added a name=home to the home url to allow access
        back to the home page via the translate.html href - see that page.  The
        urls then are this:
            url(r'^$', views.home, name='home'),
            url(r'^translate/', views.translate, name='translate')

        Then the form action becomes:
            <form action="{% url 'translate' %}"

    2. To send data from the text box to the translate page, the translate function in views.py performs a "GET" on the request:
        request.GET["originalText"]

### Translating into Pig Latin

    1. See wikipedia for the rules - Nick has his own variation.  My version works more in line with wikipedia.

    2. python split - you can test python code in the terminal:
    > python3
    >>> hello = ''Hey there my name is Nick"
    >>>hello
    'Hey there my name is Nick'
    >>> hello.split()
    ['Hey', 'there', 'my', 'name', 'is', 'Nick']
    >>>exit()

### Formatting the HTML

    1.  Added a new page, translate.html

    2. In the render call to this new page, to pass data from the home page, you
    can pass in a dictionary of strings.  In the destination web page, the
    dictionary items are accessed via {{ }} - e.g. {{originalText}}

    3. In the translate.html page, added an href to allow the user to get to
    the home page from the translate page.

### Challenge

    Create an about page.   I chose to put another button - to do so, I needed to
    check for "about" in the request - it was confusing with the method named
    translate, so I changed it to handleSubmit.  

    Nick used a <a href>
        <a href={% url 'about' % }
