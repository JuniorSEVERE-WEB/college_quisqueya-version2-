import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Article, Comment, Reaction, Tag

# --- Filtre custom pour différencier commentaires racine et réponses ---
class CommentParentFilter(admin.SimpleListFilter):
    title = "Type de commentaire"
    parameter_name = "is_root"

    def lookups(self, request, model_admin):
        return [
            ("root", "Commentaires racine"),
            ("reply", "Réponses"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "root":
            return queryset.filter(parent__isnull=True)
        if self.value() == "reply":
            return queryset.filter(parent__isnull=False)
        return queryset

# --- Admin Tag ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# --- Inline Commentaires pour Article ---
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("user", "text", "parent", "date_posted", "likes_count", "dislikes_count")
    readonly_fields = ("user", "text", "parent", "date_posted", "likes_count", "dislikes_count")
    show_change_link = True

    def likes_count(self, obj):
        return obj.reactions.filter(reaction_type="like").count()
    likes_count.short_description = "👍 Likes"

    def dislikes_count(self, obj):
        return obj.reactions.filter(reaction_type="dislike").count()
    dislikes_count.short_description = "👎 Dislikes"

# --- Inline Réactions pour Article ---
class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 0
    fields = ("user", "reaction_type", "article", "comment")
    readonly_fields = ("user", "reaction_type", "article", "comment")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# --- Admin Article ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author", "date_published",
        "is_published", "visibility",
        "likes_count", "dislikes_count",
        "comments_count",
    )
    list_filter = ("is_published", "visibility", "date_published", "tags")
    search_fields = ("title", "description", "author__username")
    readonly_fields = ("date_published",)
    ordering = ("-date_published",)
    filter_horizontal = ("tags",)
    inlines = [CommentInline, ReactionInline]
    actions = ["export_as_csv", "export_combined_csv"]

    # --- Compteurs ---
    def likes_count(self, obj):
        return obj.reactions.filter(reaction_type="like").count()
    likes_count.short_description = "👍 Likes"

    def dislikes_count(self, obj):
        return obj.reactions.filter(reaction_type="dislike").count()
    dislikes_count.short_description = "👎 Dislikes"

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = "💬 Commentaires"

    # --- Export CSV Articles simple ---
    def export_as_csv(self, request, queryset):
        field_names = ["title", "author", "date_published", "likes", "dislikes", "comments"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename=articles_export.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            writer.writerow([
                obj.title,
                obj.author.username if obj.author else "Anonyme",
                obj.date_published.strftime("%Y-%m-%d %H:%M"),
                obj.reactions.filter(reaction_type="like").count(),
                obj.reactions.filter(reaction_type="dislike").count(),
                obj.comments.count(),
            ])
        return response
    export_as_csv.short_description = "📥 Exporter en CSV (Articles sélectionnés)"

    # --- Export CSV combiné (Articles + stats + tags) ---
    def export_combined_csv(self, request, queryset):
        field_names = [
            "title", "author", "date_published",
            "article_likes", "article_dislikes",
            "comments_total", "comments_likes", "comments_dislikes",
            "tags"
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename=articles_combined_export.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            # Stats likes/dislikes sur l’article
            article_likes = obj.reactions.filter(reaction_type="like").count()
            article_dislikes = obj.reactions.filter(reaction_type="dislike").count()

            # Stats commentaires liés
            comments_total = obj.comments.count()
            comments_likes = Reaction.objects.filter(comment__article=obj, reaction_type="like").count()
            comments_dislikes = Reaction.objects.filter(comment__article=obj, reaction_type="dislike").count()

            # Tags associés
            tags = ", ".join([t.name for t in obj.tags.all()])

            writer.writerow([
                obj.title,
                obj.author.username if obj.author else "Anonyme",
                obj.date_published.strftime("%Y-%m-%d %H:%M"),
                article_likes,
                article_dislikes,
                comments_total,
                comments_likes,
                comments_dislikes,
                tags,
            ])
        return response
    export_combined_csv.short_description = "📊 Export combiné (Articles + stats + tags)"

# --- Admin Commentaire ---
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "article", "user", "short_text",
        "date_posted", "parent",
        "likes_count", "dislikes_count",
    )
    search_fields = ("text", "user__username", "article__title")
    list_filter = ("date_posted", "article", CommentParentFilter)
    readonly_fields = ("date_posted",)
    ordering = ("-date_posted",)
    actions = ["delete_selected", "export_comments_csv"]

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "🗑️ Supprimer les commentaires sélectionnés"

    def likes_count(self, obj):
        return obj.reactions.filter(reaction_type="like").count()
    likes_count.short_description = "👍 Likes"

    def dislikes_count(self, obj):
        return obj.reactions.filter(reaction_type="dislike").count()
    dislikes_count.short_description = "👎 Dislikes"

    def short_text(self, obj):
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")
    short_text.short_description = "Commentaire"

    # --- Export CSV Commentaires ---
    def export_comments_csv(self, request, queryset):
        field_names = ["article", "user", "text", "date_posted", "parent", "likes", "dislikes"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename=comments_export.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            writer.writerow([
                obj.article.title,
                obj.user.username if obj.user else "Anonyme",
                obj.text.replace("\n", " ")[:200],
                obj.date_posted.strftime("%Y-%m-%d %H:%M"),
                obj.parent.id if obj.parent else "",
                obj.reactions.filter(reaction_type="like").count(),
                obj.reactions.filter(reaction_type="dislike").count(),
            ])
        return response
    export_comments_csv.short_description = "📥 Exporter en CSV (Commentaires sélectionnés)"

# --- Admin Réaction ---
@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "reaction_type", "article", "comment")
    list_filter = ("reaction_type", "article", "comment")
    search_fields = ("user__username", "article__title")
    ordering = ("-id",)
    actions = ["export_reactions_csv"]

    # --- Export CSV Réactions ---
    def export_reactions_csv(self, request, queryset):
        field_names = ["user", "reaction_type", "article", "comment"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename=reactions_export.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            writer.writerow([
                obj.user.username if obj.user else "Anonyme",
                obj.reaction_type,
                obj.article.title if obj.article else "",
                f"Comment {obj.comment.id}" if obj.comment else "",
            ])
        return response
    export_reactions_csv.short_description = "📥 Exporter en CSV (Réactions sélectionnées)"
