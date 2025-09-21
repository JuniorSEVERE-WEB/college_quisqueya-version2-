from rest_framework import serializers
from .models import Article, Comment, Reaction, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id", "title", "image", "description", "date_published",
            "is_published", "visibility", "author", "tags",
            "likes_count", "dislikes_count"
        ]
        read_only_fields = ["date_published"]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "article", "user", "parent", "text", "date_posted"]
        read_only_fields = ["date_posted"]

    def validate(self, attrs):
        parent = attrs.get("parent")
        article = attrs.get("article")
        if parent and parent.article_id != article.id:
            raise serializers.ValidationError("Le parent doit appartenir au même article.")
        return attrs

class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reaction
        fields = ["id", "user", "article", "comment", "reaction_type"]

    def validate(self, attrs):
        article = attrs.get("article")
        comment = attrs.get("comment")
        if not article and not comment:
            raise serializers.ValidationError("Spécifie article OU comment.")
        if article and comment:
            raise serializers.ValidationError("Spécifie soit article, soit comment, pas les deux.")
        return attrs