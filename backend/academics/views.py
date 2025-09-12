from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ArticleForm, CommentForm
from .models import Article, Comment

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
    comments = article.comments.filter(parent__isnull=True)
    comment_form = CommentForm()
    return render(request, "blog/article_detail.html", {
        "article": article,
        "comments": comments,
        "comment_form": comment_form,
    })

def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect("blog_article_detail", pk=article.pk)
    return redirect("blog_article_detail", pk=article.pk)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user == request.user or request.user.is_staff:
        article_pk = comment.article.pk
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect("blog_article_detail", pk=article_pk)
    messages.error(request, "You do not have permission to delete this comment.")
    return redirect("blog_article_detail", pk=comment.article.pk)