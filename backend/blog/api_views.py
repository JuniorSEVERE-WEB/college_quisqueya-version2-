from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Article, Comment, Reaction, Tag
from .serializers import ArticleSerializer, CommentSerializer, ReactionSerializer, TagSerializer
from rest_framework.pagination import PageNumberPagination

class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass

from rest_framework.permissions import AllowAny

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_published=True).order_by("-date_published")
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]  # 👈 Tout le monde peut lire



    # 🔹 Ajouts DRF pour filtrage et recherche
    filterset_fields = ["is_published", "visibility", "tags", "category"]
    search_fields = ["title", "description"]
    ordering_fields = ["date_published", "id"]

    def get_queryset(self):
        qs = super().get_queryset()

        # Afficher uniquement les articles publiés si pas admin
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            qs = qs.filter(is_published=True)

        # Filtrer par tag si présent
        tag_id = self.request.query_params.get("tag")
        if tag_id:
            qs = qs.filter(tags__id=tag_id)

        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentPagination(PageNumberPagination):
    page_size = 10  # 10 commentaires par défaut
    page_size_query_param = "page_size"
    max_page_size = 100


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("article", "user").all().order_by("-date_posted")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination  

    # Ajouts DRF
    filterset_fields = ["article", "user", "parent"]
    search_fields = ["text"]
    ordering_fields = ["date_posted", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        article_id = self.request.query_params.get("article")
        if article_id:
            qs = qs.filter(article_id=article_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related("article", "comment", "user").all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ajouts DRF
    filterset_fields = ["article", "comment", "user", "reaction_type"]
    ordering_fields = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()
        article_id = self.request.query_params.get("article")
        comment_id = self.request.query_params.get("comment")
        if article_id:
            qs = qs.filter(article_id=article_id)
        if comment_id:
            qs = qs.filter(comment_id=comment_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Ajouts DRF
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name", "id"]
