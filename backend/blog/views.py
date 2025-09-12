# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ArticleForm, CommentForm
from .models import Article, Comment, Reaction, Tag
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# --- Article views déjà existantes ---
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("blog_article_detail", pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, "blog/add_article.html", {"form": form})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Gestion des commentaires
    comments_list = Comment.objects.filter(article=article, parent__isnull=True).order_by("-date_posted")
    paginator = Paginator(comments_list, 5)  # 5 commentaires par page
    page_number = request.GET.get("page")
    comments = paginator.get_page(page_number)

    # Gestion de la pagination des réponses et création du dictionnaire
    replies_paginated = {}
    for comment in comments:
        replies_list = comment.replies.all().order_by("date_posted")
        reply_paginator = Paginator(replies_list, 3)  # 3 réponses par page
        reply_page_number = request.GET.get("reply_page")
        comment_id = request.GET.get("comment")

        if comment_id and int(comment_id) == comment.id:
            replies_paginated[comment.pk] = reply_paginator.get_page(reply_page_number)
        else:
            replies_paginated[comment.pk] = reply_paginator.get_page(1)

    # Gestion du formulaire d'ajout de commentaire
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get("parent")
            parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.parent = parent
            new_comment.save()
            return redirect("blog_article_detail", pk=article.pk)
    else:
        form = CommentForm()

    return render(request, "blog/article_detail.html", {
        "article": article,
        "comments": comments,
        "comment_form": form,
        "replies_paginated": replies_paginated,
    })





def articles_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    articles = tag.articles.filter(is_published=True).order_by("-date_published")
    return render(request, "blog/articles_by_tag.html", {"tag": tag, "articles": articles})


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect("blog_article_detail", pk=article.pk)
    return redirect("blog_article_detail", pk=article.pk)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user or request.user.is_staff:
        article_pk = comment.article.pk
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect("blog_article_detail", pk=article_pk)
    messages.error(request, "You do not have permission to delete this comment.")
    return redirect("blog_article_detail", pk=comment.article.pk)


# --- NEW: gérer les likes/dislikes ---
def toggle_reaction(request, content_type, pk, reaction_type):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour réagir.")
        return redirect("blog_article_detail", pk=pk)

    if content_type == "article":
        target = get_object_or_404(Article, pk=pk)
        reaction, created = Reaction.objects.get_or_create(
            user=request.user, article=target, comment=None,
            defaults={"reaction_type": reaction_type}
        )
    elif content_type == "comment":
        target = get_object_or_404(Comment, pk=pk)
        reaction, created = Reaction.objects.get_or_create(
            user=request.user, article=None, comment=target,
            defaults={"reaction_type": reaction_type}
        )
    else:
        messages.error(request, "Type de contenu invalide.")
        return redirect("blog_article_detail", pk=pk)

    # Si la réaction existe mais n’est pas la même, on la met à jour
    if not created:
        if reaction.reaction_type == reaction_type:
            reaction.delete()  # toggle off
        else:
            reaction.reaction_type = reaction_type
            reaction.save()

    # Rediriger vers l’article parent
    if content_type == "article":
        return redirect("blog_article_detail", pk=target.pk)
    else:
        return redirect("blog_article_detail", pk=target.article.pk)
    


def articles_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    articles = Article.objects.filter(tags=tag, is_published=True)

    return render(request, "blog/articles_by_tag.html", {
        "tag": tag,
        "articles": articles
    })
