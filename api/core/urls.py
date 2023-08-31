from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("core/users", views.UserModelViewSet)
router.register("core/departments", views.DepartmentViewSet)

urlpatterns = router.urls
