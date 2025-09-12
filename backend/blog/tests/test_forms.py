from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.forms import ArticleForm, CommentForm
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class BlogFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user3", password="pass", email="user3@test.ht")

    def test_article_form_valid(self):
        """Le formulaire ArticleForm est valide avec tous les champs requis"""
        form_data = {
            "title": "Titre test",
            "description": "Description test",
            "visibility": "all",  # correspond à ton modèle
            "is_published": True,
        }
        file_data = {
            "image": SimpleUploadedFile(
                "test.gif",
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
                content_type="image/gif"
            )
        }
        form = ArticleForm(data=form_data, files=file_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_article_form_missing_fields(self):
        """Le formulaire ArticleForm est invalide si un champ obligatoire manque"""
        form_data = {
            "description": "Description test",
            "visibility": "all",
            "is_published": True,
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("image", form.errors)

    def test_comment_form_valid(self):
        """Le formulaire CommentForm est valide avec le texte"""
        form_data = {"text": "Un commentaire"}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_missing_text(self):
        """Le formulaire CommentForm est invalide si le texte est vide"""
        form_data = {"text": ""}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("text", form.errors)