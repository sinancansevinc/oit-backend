from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("values/value", views.ValueViewSet)
router.register("values/valueassessment", views.ValueAssessmentViewSet)


urlpatterns = router.urls
