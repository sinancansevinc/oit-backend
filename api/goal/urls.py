from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("goals/goal", views.GoalViewSet)

urlpatterns = router.urls
