#===============================================================================
# :App:         blog
# :Module:      models
# :Author:      Stuart Cox (stuart.cox@gmail.com)
# :Copyright:   public domain
#===============================================================================
"""Models for blog app."""

__docformat__ = "restructuredtext"

from django.db import models
from google.appengine.ext import db


class User(db.Model):
    """
    A blog user. To be used for editors, VIP visitors, mailing list members etc.
    """
    name = db.StringProperty(required=True)
    nickname = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)


class PostImage(db.Model):
    """
    An image for use in a post. Currently just used for title images, but
    could also be used for incidental images.
    """
    file = db.BlobProperty(required=True)
    caption = db.StringProperty(required=True)
    alt = db.StringProperty(required=True)


class Post(db.Model):
    """A blog post with all associated metadata."""
    ## Fields ##
    content = db.TextProperty(required=True)
    title = db.StringProperty(required=True)
    summary = db.StringProperty(required=True)
    author = db.ReferenceProperty(User)
    image = db.ReferenceProperty(PostImage)
    pubDate = db.DateTimeProperty("date published", required=True)
    lastMod = db.DateTimeProperty("last modified", required=True)
    slug = db.StringProperty(required=True)
    
    @models.permalink
    def get_absolute_url(self):
        """Return post's display page URL"""
        return ("blog:view-post", (), {'slug': self.slug})

    @models.permalink
    def get_absolute_edit_url(self):
        """Return post's edit page URL"""
        # If a slug is defined, redirect to the edit page for that slug,
        # otherwise redirect to the new post page
        if self.slug:
            return ("blog:edit-post", (), {'slug': self.slug})
        else:
            return ("blog:new-post", (), {})
