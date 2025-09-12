from django.contrib import admin
from .models import Article, Comment, Reaction, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_published", "is_published", "visibility", "likes_count", "dislikes_count")
    list_filter = ("is_published", "visibility", "date_published", "tags")
    search_fields = ("title", "description")
    readonly_fields = ("date_published",)
    ordering = ("-date_published",)
    filter_horizontal = ("tags",) 

    def likes_count(self, obj):
        return obj.reactions.filter(type="like").count()
    likes_count.short_description = "👍 Likes"

    def dislikes_count(self, obj):
        return obj.reactions.filter(type="dislike").count()
    dislikes_count.short_description = "👎 Dislikes"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "text", "date_posted", "parent", "likes_count", "dislikes_count")
    search_fields = ("text", "user__username", "article__title")
    list_filter = ("date_posted", "article")
    readonly_fields = ("date_posted",)
    ordering = ("-date_posted",)
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Supprimer les commentaires sélectionnés"

    def likes_count(self, obj):
        return obj.reactions.filter(type="like").count()
    likes_count.short_description = "👍 Likes"

    def dislikes_count(self, obj):
        return obj.reactions.filter(type="dislike").count()
    dislikes_count.short_description = "👎 Dislikes"
