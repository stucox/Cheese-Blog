#===============================================================================
# :App:         blog
# :Module:      urls
# :Author:      Stuart Cox (stuart.cox@gmail.com)
# :Copyright:   public domain
#===============================================================================
"""
URL mapping for this app:
- /                                   list of posts with summaries ("home" page)
- /post/<slug>/                       display post
- /ctrl/                              control panel
- /ctrl/new-post/                     new post form
- /ctrl/edit-post/<slug>/             edit post form
"""
__docformat__ = "restructuredtext"

from django.conf.urls.defaults import patterns, url
from blog.views import PostOrder

# HTML URL view mapping for this app:
urlpatterns = patterns("blog.views",
    url(r"^$", "listPosts", name="list-posts",
            kwargs={'max': 10, 'order': PostOrder.NEWEST_FIRST}),
    url(r"^post/(?P<slug>.+)/$", "viewPost", name="view-post"),
    url(r"^ctrl/$", "ctrlPanel", name="ctrl-panel",
            kwargs={'order': PostOrder.NEWEST_FIRST}),
    url(r"^ctrl/new-post/$", "editPost", name="new-post"),
    url(r"^ctrl/edit-post/(?P<slug>[A-Za-z0-9_-]+)/$", "editPost",
            name="edit-post"),
    # Special 'view post' URL with no slug to allow reversal of a 'base' post
    # display URL, e.g. /post/ - if this is requested, the view function should
    # ensure a 404 is returned, but could be replaced with an appropriate valid
    # page    
    url(r"^post/$", "viewPost", name="view-post-base", kwargs={'slug':None}),
)
