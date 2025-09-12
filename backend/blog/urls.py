# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Articles
    path("article/add/", views.add_article, name="blog_add_article"),
    path("article/<int:pk>/", views.article_detail, name="blog_article_detail"),

    # Commentaires
    path("article/<int:article_id>/comment/", views.add_comment, name="blog_add_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="blog_delete_comment"),

    # Réactions
    path("article/<int:pk>/<str:reaction_type>/", views.toggle_reaction, {"content_type": "article"}, name="blog_article_reaction"),
    path("comment/<int:pk>/<str:reaction_type>/", views.toggle_reaction, {"content_type": "comment"}, name="blog_comment_reaction"),


        # ...autres routes...
    path("<int:pk>/reaction/<str:reaction_type>/", views.toggle_reaction, {"content_type": "article"}, name="blog_like_article"),
    # Pour les commentaires :
    path("comment/<int:pk>/reaction/<str:reaction_type>/", views.toggle_reaction, {"content_type": "comment"}, name="blog_like_comment"),

    #tags
    path("tag/<int:tag_id>/", views.articles_by_tag, name="blog_articles_by_tag"),
]
