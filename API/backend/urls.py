from rest_framework.routers import DefaultRouter

from backend.views import AllRecordingView

router = DefaultRouter()
router.register("all", AllRecordingView)

urlpatterns = router.urls
