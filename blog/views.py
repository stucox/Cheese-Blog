#===============================================================================
# :App:         blog
# :Module:      views
# :Author:      Stuart Cox (stuart.cox@gmail.com)
# :Copyright:   public domain
#===============================================================================
"""
Views of blogs app. All functions are designed to be called by URL resolution
and return HTTP responses.
"""
__docformat__ = "restructuredtext"

import datetime

from django.forms import ModelForm, FileInput
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from blog.models import Post, PostImage

# Template files used by views in this module
EDIT_POST_TEMPLATE = "blog/edit-post.html"
VIEW_POST_TEMPLATE = "blog/view-post.html"
LIST_POSTS_TEMPLATE = "blog/list-posts.html"
CTRL_PANEL_TEMPLATE = "blog/ctrl-panel.html"

class PostOrder(object):
    """Post sort orders, used when multiple posts are viewed"""
    NEWEST_FIRST = "-pubDate"
    OLDEST_FIRST = "pubDate"
    RANDOM = "?"


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'summary', 'content')


#########################
## HTML View Functions ##
#########################

def listPosts(request, max=None, order=PostOrder.NEWEST_FIRST):
    """
    A list of the posts in the blog, with summaries and links to each.
    
    Parameters:
    - `request`: a `WSGIRequest` representing the HTTP request for this view
    - `max`: the maximum number of posts to display, or None to display all
      posts
    - `order`: a member of the PostOrder enum class defining the sorting order
      of posts in the list; defaults to newest first.
    """
    posts = Post.objects.all().order_by(order)[:max]
    return render_to_response(LIST_POSTS_TEMPLATE, {'posts': posts},
            context_instance=RequestContext(request))

def editPost(request, slug=None):
    """
    Admin interface for creating and editing blog posts.
    
    Parameters:
    - `request`: a `WSGIRequest` representing the HTTP request for this view
    - `slug`: the URL slug of the post to edit, or None to create a new post
    """
    ## This view function handles post creation, editing, deletion and display
    ## of edit interfaces
    # Create a list of success messages to be updated
    successes = []
    # If no URL slug is provided, it's a new blog post
    isNewPost = slug is None
    # If it's a new post, create an empty instance to play with; this will only
    # be written to the database if data has been submitted
    if isNewPost:
        post = Post()
    # If not a new post, try to get the blog post with the provided slug
    else:
        post = get_object_or_404(Post, slug=slug)
    # If there's POST data, changes have been submitted so create/update the
    # post
    if request.method == "POST":
        # Parse the POST data with the form then store validated fields
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            # Create a post instance using the validated form data
            post = form.save(commit=False)
            # Add fields which don't come from the form
            post.lastMod = datetime.datetime.now()
            # Only set the publish date and slug if this is a new post; these
            # can't be changed afterwards
            if isNewPost:
                post.pubDate = datetime.datetime.now()
                post.slug = getUniquePostSlug(form.cleaned_data['title'])
            # Changes have only been made to instances in memory, so save to
            # database
            post.save()
            # Add a message to the success list
            successes.append("Post created successfully." if isNewPost else \
                    "Post updated successfully.")
            #return redirect("blog:edit-post", slug=post.slug)
    else:
        # If not a new post, create a form bound to the instance grabbed earlier
        if not isNewPost:
            form = PostEditForm(instance=post)
        # Otherwise create an unbound form to build the page with
        else:
            form = PostEditForm()
    # Render and return the edit form as a response
    return render_to_response(EDIT_POST_TEMPLATE, {'post': post, 'form': form,
            'successes': successes}, context_instance=RequestContext(request))

def viewPost(request, slug):
    """
    Display a blog post.
    
    Parameters:
    - `request`: a `WSGIRequest` representing the HTTP request for this view
    - `slug`: the URL slug of the post to edit, or None to create a new post
    """
    if slug is None:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    return render_to_response(VIEW_POST_TEMPLATE, {'post': post},\
            context_instance=RequestContext(request))
    
def ctrlPanel(request, order=PostOrder.NEWEST_FIRST):
    """
    Control panel for blog administration.
    
    Parameters:
    - `request`: a `WSGIRequest` representing the HTTP request for this view
    - `order`: a member of the PostOrder enum class defining the sorting order
      of posts in the list; defaults to newest first.
    """
    posts = Post.objects.all().order_by(order)
    # If the request contains POST data, perform any necessary post deletions
    if request.method == "POST":
        for slug in request.POST.getlist('delete'):
            posts.get(slug=slug).delete()
    return render_to_response(CTRL_PANEL_TEMPLATE, {'posts': posts},\
            context_instance=RequestContext(request))

def dlPostImage(request, pk):
    """Download handler for serving uploaded post images."""
    upload = get_object_or_404(PostImage, pk=pk)
    return serve_file(request, upload.file)


######################
## HELPER FUNCTIONS ##
######################

def getUniquePostSlug(srcString, disallowed=[]):
    """
    Generates a valid, unique, available slug based on a source string (e.g.
    a post summary.
    
    Parameters:
    - `srcString`: a string from which to generate the slug
    - `disallowed`: a list of string which should not be allowed as slugs
    """
    # Find an unused slug by suffixing with numbers until we find one which
    # doesn't already exist
    suffixNum = 0
    while True:
        suffix = "-%d" % suffixNum if suffixNum else ""
        slug = slugify(srcString + suffix)
        if not checkPostSlug(slug, disallowed):
            break
        suffixNum += 1
    return slug

def checkPostSlug(slug, disallowed=[]):
    """
    Checks is a post slug is valid, unique and available.
    
    Parameters:
    - `slug`: the slug string to check
    - `disallowed`: a list of string which should not be allowed as slugs
    """
    # TODO: thorough checking of slug format
    return Post.objects.filter(slug=slug).exists() and not slug in disallowed

def saveImageFile(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
