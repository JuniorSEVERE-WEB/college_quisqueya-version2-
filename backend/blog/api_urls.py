from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, CommentViewSet, ReactionViewSet, TagViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="article")
router.register("comments", CommentViewSet, basename="comment")
router.register("reactions", ReactionViewSet, basename="reaction")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls