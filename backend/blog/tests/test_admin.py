from django.test import TestCase
from django.contrib import admin
from blog.models import Article, Comment
from blog.admin import ArticleAdmin, CommentAdmin

class TestBlogAdmin(TestCase):
    def test_article_admin_registered(self):
        """Vérifie que le modèle Article est bien enregistré dans l'admin"""
        self.assertIn(Article, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Article], ArticleAdmin)

    def test_comment_admin_registered(self):
        """Vérifie que le modèle Comment est bien enregistré dans l'admin"""
        self.assertIn(Comment, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Comment], CommentAdmin)