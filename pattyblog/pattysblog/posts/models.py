from django.db import models

# Create your models here.


class Post(models.Model):

    # Atttibutes must have types - see the django doc for
    # the various attribute types.

    title = models.CharField(max_length=250)
    publishedDate = models.DateTimeField()

    # Give a folder where the images will be stored.
    image = models.ImageField(upload_to='media/')

    # The post text.
    body = models.TextField()

    # This is used to rename a post from Post Object to the title of the
    # post.
    def __str__(self):
        return self.title

    # Return a formatted date
    def publishedDatePretty(self):
        return self.publishedDate.strftime("%b %e %Y")

    # Return a summary of the body text
    def bodySummary(self):
        return self.body[:100]
