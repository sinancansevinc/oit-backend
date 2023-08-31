from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self) -> None:
        from core.urls import router
        from oit_backend.router import router as main_router

        main_router.extend(router)