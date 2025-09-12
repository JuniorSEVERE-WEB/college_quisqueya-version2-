from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Article, Comment

User = get_user_model()

class TestBlogPermissions(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user1", password="pass", email="user1@test.ht")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass", email="admin@test.ht")
        self.other_user = User.objects.create_user(username="user2", password="pass", email="user2@test.ht")
        self.article = Article.objects.create(
            title="Test Article",
            image="test.jpg",
            description="Test description",
            is_published=True,
            visibility="all",
            author=self.user
        )
        self.comment = Comment.objects.create(
            article=self.article,
            user=self.user,
            text="Premier commentaire"
        )

    def test_only_owner_or_admin_can_delete_comment(self):
        # Auteur connecté
        self.client.login(username="user1", password="pass")
        response = self.client.post(reverse("blog_delete_comment", args=[self.comment.pk]))
        self.assertRedirects(response, reverse("blog_article_detail", args=[self.article.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

        # Recrée le commentaire pour les autres tests
        self.comment = Comment.objects.create(
            article=self.article,
            user=self.user,
            text="Premier commentaire"
        )

        # Autre utilisateur connecté
        self.client.login(username="user2", password="pass")
        response = self.client.post(reverse("blog_delete_comment", args=[self.comment.pk]))
        self.assertRedirects(response, reverse("blog_article_detail", args=[self.article.pk]))
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

        # Admin connecté
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("blog_delete_comment", args=[self.comment.pk]))
        self.assertRedirects(response, reverse("blog_article_detail", args=[self.article.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_only_authenticated_user_can_comment(self):
        # Utilisateur non connecté
        response = self.client.post(reverse("blog_add_comment", args=[self.article.pk]), {"text": "Test"})
        self.assertEqual(response.status_code, 302)  # Redirection vers login ou refus

        # Utilisateur connecté
        self.client.login(username="user2", password="pass")
        response = self.client.post(reverse("blog_add_comment", args=[self.article.pk]), {"text": "Test"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(text="Test").exists())

    def test_only_authenticated_user_can_like_article(self):
        # Utilisateur non connecté
        response = self.client.get(reverse("blog_like_article", args=[self.article.pk, "like"]))
        self.assertIn(response.status_code, [302, 403])  # Redirection ou refus

        # Utilisateur connecté
        self.client.login(username="user2", password="pass")
        response = self.client.get(reverse("blog_like_article", args=[self.article.pk, "like"]))
        self.assertIn(response.status_code, [200, 302])