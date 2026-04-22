from rest_framework.routers import DefaultRouter
from .views import FrameworkViewSet, ObligationViewSet, ClauseViewSet, ControlViewSet, EvidenceViewSet

router = DefaultRouter()
router.register('frameworks', FrameworkViewSet)
router.register('obligations', ObligationViewSet)
router.register('clauses', ClauseViewSet)
router.register('controls', ControlViewSet)
router.register(r'evidence', EvidenceViewSet, basename='evidence')

urlpatterns = router.urls