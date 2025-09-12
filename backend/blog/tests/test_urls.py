from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog import views

class BlogUrlsTests(SimpleTestCase):
    def test_blog_add_article_url(self):
        url = reverse("blog_add_article")
        self.assertEqual(resolve(url).func, views.add_article)

    def test_blog_article_detail_url(self):
        url = reverse("blog_article_detail", args=[1])
        self.assertEqual(resolve(url).func, views.article_detail)

    def test_blog_add_comment_url(self):
        url = reverse("blog_add_comment", args=[1])
        self.assertEqual(resolve(url).func, views.add_comment)

    def test_blog_delete_comment_url(self):
        url = reverse("blog_delete_comment", args=[1])
        self.assertEqual(resolve(url).func, views.delete_comment)