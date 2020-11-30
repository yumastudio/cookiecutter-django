from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG)), name="graphql"),
    path("uploads/", include('ckeditor_uploader.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
