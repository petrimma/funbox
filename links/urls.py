from django.urls import path

from .views import get_visited_domains, post_visited_links


urlpatterns = [
    path("visited_links/", post_visited_links, name="visited_links"),
    path("visited_domains/", get_visited_domains, name="visited_domains"),
]
