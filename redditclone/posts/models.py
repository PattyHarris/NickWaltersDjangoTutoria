from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    # Atttibutes must have types - see the django doc for
    # the various attribute types.  We could have used an URLField here as
    # well as a SmallIntegerField or Positive..IntegerField.

    title = models.CharField(max_length=200)
    publishedDate = models.DateTimeField()
    url = models.TextField()
    author = models.ForeignKey(User)
    votesTotal = models.IntegerField(default=1)

    # This is used to rename a post from Post Object to the title of the
    # post.
    def __str__(self):
        return self.title

    # Return a formatted date
    def publishedDatePretty(self):
        return self.publishedDate.strftime("%b %e %Y")
