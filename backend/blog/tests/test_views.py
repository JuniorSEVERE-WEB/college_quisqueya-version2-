from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Article, Comment, Reaction
from blog.forms import ArticleForm, CommentForm

User = get_user_model()

class BlogViewsTests(TestCase):
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
        self.reply = Comment.objects.create(
            article=self.article,
            user=self.other_user,
            text="Réponse au commentaire",
            parent=self.comment
        )

    def test_comment_reply(self):
        self.assertEqual(self.reply.parent, self.comment)
        self.assertEqual(self.reply.article, self.article)

    def test_owner_can_delete_comment(self):
        self.client.login(username="user1", password="pass")
        response = self.client.post(reverse("blog_delete_comment", args=[self.comment.pk]))
        self.assertRedirects(response, reverse("blog_article_detail", args=[self.article.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_admin_can_delete_comment(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("blog_delete_comment", args=[self.reply.pk]))
        self.assertRedirects(response, reverse("blog_article_detail", args=[self.article.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.reply.pk).exists())

    def test_other_user_cannot_delete_comment(self):
        self.client.login(username="user2", password="pass")
        response = self.client.post(reverse("blog_delete_comment", args=[self.comment.pk]))
        self.assertRedirects(response, reverse("blog_article_detail", args=[self.article.pk]))
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_urls_exist(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(reverse("blog_add_article"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("blog_article_detail", args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("blog_add_comment", args=[self.article.pk]), {"text": "Nouveau commentaire"})
        self.assertEqual(response.status_code, 302)

    def test_like_article_view(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(reverse("blog_like_article", args=[self.article.pk, "like"]))
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        # Ajoute une vérification sur Reaction si tu utilises ce modèle

    def test_dislike_comment_view(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(reverse("blog_like_comment", args=[self.comment.pk, "dislike"]))
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        # Ajoute une vérification sur Reaction si tu utilises ce modèle

class ReactionViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user1", password="pass", email="user1@test.ht")
        self.other_user = User.objects.create_user(username="user2", password="pass", email="user2@test.ht")
        self.article = Article.objects.create(
            title="Article avec réactions",
            image="test.jpg",
            description="Description",
            is_published=True,
            visibility="all",
            author=self.user
        )
        self.comment = Comment.objects.create(
            article=self.article,
            user=self.other_user,
            text="Un commentaire test"
        )

    def test_user_can_like_article(self):
        reaction = Reaction.objects.create(user=self.user, article=self.article, reaction_type="like")
        self.assertEqual(self.article.reactions.filter(reaction_type="like").count(), 1)
        self.assertEqual(reaction.reaction_type, "like")

    def test_user_can_dislike_comment(self):
        reaction = Reaction.objects.create(user=self.user, comment=self.comment, reaction_type="dislike")
        self.assertEqual(self.comment.reactions.filter(reaction_type="dislike").count(), 1)
        self.assertEqual(reaction.reaction_type, "dislike")

    def test_user_can_change_reaction(self):
        reaction = Reaction.objects.create(user=self.user, article=self.article, reaction_type="like")
        reaction.reaction_type = "dislike"
        reaction.save()
        self.assertEqual(self.article.reactions.filter(reaction_type="like").count(), 0)
        self.assertEqual(self.article.reactions.filter(reaction_type="dislike").count(), 1)

    def test_two_users_like_same_article(self):
        Reaction.objects.create(user=self.user, article=self.article, reaction_type="like")
        Reaction.objects.create(user=self.other_user, article=self.article, reaction_type="like")
        self.assertEqual(self.article.reactions.filter(reaction_type="like").count(), 2)