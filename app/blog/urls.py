from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("snippets/", views.snippet_list, name="snippet_list"),
    path("snippets/<int:pk>/", views.snippet_detail, name="snippet_detail"),
    path("errors/", views.error_list, name="error_list"),
    path("errors/<int:pk>/", views.error_detail, name="error_detail"),
    path("tutorials/", views.tutorial_list, name="tutorial_list"),
    path("tutorials/<int:pk>/", views.tutorial_detail, name="tutorial_detail"),
    path("demos/", views.demo_list, name="demo_list"),
    path("demos/<int:pk>/", views.demo_detail, name="demo_detail"),
    path(
        "comment/<str:content_type_name>/<int:object_id>/",
        views.post_comment,
        name="post_comment",
    ),
]
