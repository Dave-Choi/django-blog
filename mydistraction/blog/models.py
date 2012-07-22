from django.db import models
from datetime import datetime
import markdown
import re


# Accept lowercase alphanumerics, dash and underscores only.
# I don't know if there's a better way to do this.  Ideally, I'd like to nest the compiled regex into another
author_name_max_length = 100
author_name_pattern = '[a-z0-9_-]{1,%d}' % author_name_max_length
author_slug_pattern = '[a-zA-Z0-9_-]{1,%d}' % author_name_max_length


class Author(models.Model):
    # Single field for names.  Names are unique and can't have whitespace to avoid confusion.

    # TODO - Consider storing blurb as HTML/Markdown - May be outside the scope of the author model

    # display_name is the client facing version of the name, and what a user enters when they create a new author account
    #   - The actual name field is generated as a lowercase version and must be unique.
    #   - This allows users to enter mixed case names, but ones that are case insensitive unique
    #       - This is probably a stupid way to do this, when you can do it with a DB constraint, but this is DB agnostic.
    #   - display_name is also used as a slug
    name = models.CharField(max_length=author_name_max_length, unique=True, editable=False)
    display_name = models.SlugField(max_length=author_name_max_length, unique=True)

    blurb = models.TextField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.display_name.lower()
        if(re.match('^%s$' % author_name_pattern, self.name)):
            return super(Author, self).save(*args, **kwargs)
        raise Exception("Attempting to save an Author with invalid name.")


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
        return super(Post, self).save(*args, **kwargs)
