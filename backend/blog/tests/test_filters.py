from django.test import SimpleTestCase
from blog.templatetags.custom_filters import get_item

class TestCustomFilters(SimpleTestCase):
    def test_get_item_returns_value(self):
        d = {"a": 1, "b": 2}
        self.assertEqual(get_item(d, "a"), 1)
        self.assertEqual(get_item(d, "b"), 2)

    def test_get_item_returns_none_for_missing_key(self):
        d = {"a": 1}
        self.assertIsNone(get_item(d, "z"))