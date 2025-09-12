from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "image", "description", "visibility", "is_published")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", "parent")