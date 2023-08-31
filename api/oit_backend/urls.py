from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from oit_backend.router import router
from core.views import GoogleAuthView, LogoutView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

urlpatterns += i18n_patterns(
    path("api/", include(router.urls)),
    path("api/login/", GoogleAuthView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    prefix_default_language=False,
)
