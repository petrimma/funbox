from django.urls import path

from .views import LinkViewSet


urlpatterns = [
    path("visited_links/",
         LinkViewSet.as_view({"post": "create"}), name="visited_links"),
    path("visited_domains/",
         LinkViewSet.as_view({"get": "list"}), name="visited_domains"),
]
