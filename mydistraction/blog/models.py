from django.db import models
from datetime import datetime
import markdown
import re

# Accept lowercase alphanumerics, dash and underscores only.
# I don't know if there's a better way to do this.  Ideally, I'd like to nest the compiled regex into another
author_name_max_length = 100
author_name_pattern = '[a-z0-9_-]{1,%d}' % author_name_max_length


class Author(models.Model):
    # Single field for names.  Names are unique and can't have whitespace to avoid confusion.
    # TODO - Overload save method to reject names with whitespace - Don't trim or alter.  Just reject it.
    # TODO - Add check for the name to match authorNamePattern
    name = models.CharField(max_length=author_name_max_length, unique=True)
    blurb = models.TextField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300)
    date_created = models.DateTimeField(default=datetime.now)
    date_published = models.DateTimeField()
    is_published = models.BooleanField()
    body_html = models.TextField(editable=False)
    body_markdown = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True)  # blank and null are required to make the FK optional.
    author = models.ForeignKey(Author)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = markdown.markdown(self.body_markdown)
        super(Post, self).save(*args, **kwargs)
