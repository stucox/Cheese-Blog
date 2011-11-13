#===============================================================================
# :Project:     cheese
# :Module:      urls
# :Author:      Stuart Cox (stuart.cox@gmail.com)
# :Copyright:   public domain
#===============================================================================
"""
URL mapping for this project: forward all URL requests to the blog app.
"""
__docformat__ = "restructuredtext"

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("",
    # tinymce wysiwyg editor URLs
    url(r"^tinymce/", include("tinymce.urls")),
    # Forward all other URL requests to blog app
    url(r"^", include("blog.urls", namespace="blog", app_name="blog")),
)
