#===============================================================================
# :App:         blog
# :Module:      models
# :Author:      Stuart Cox (stuart.cox@gmail.com)
# :Copyright:   public domain
#===============================================================================
"""Models used by blog app."""

__docformat__ = "restructuredtext"

import os

from django.core.urlresolvers import reverse
from django.db import models


class User(models.Model):
    """
    A blog user. To be used for editors, VIP visitors, mailing list members etc.
    """
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    email = models.EmailField()


class PostImage(models.Model):
    """
    An image for use in a post. Currently just used for title images, but
    could also be used for incidental images.
    """
    file = models.ImageField(upload_to="blog/post-images/")
    caption = models.CharField(max_length=200, blank=True)
    alt = models.CharField(max_length=100, blank=True)


class Post(models.Model):
    """A blog post with all associated metadata."""
    ## Fields ##
    content = models.TextField()
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True)
    image = models.ForeignKey(PostImage, null=True)
    pubDate = models.DateTimeField("date published")
    lastMod = models.DateTimeField("last modified")
    slug = models.SlugField(primary_key=True)
    
    @models.permalink
    def get_absolute_url(self):
        """Return post's display page URL"""
        return ("blog:view-post", (), {'slug': self.slug})

    @models.permalink
    def get_absolute_edit_url(self):
        """Return post's edit page URL"""
        if self.slug:
            return ("blog:edit-post", (), {'slug': self.slug})
        else:
            return ("blog:new-post", (), {})
