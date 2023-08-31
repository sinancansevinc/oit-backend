from django.apps import AppConfig


class ValueassessmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'valueassessment'

    def ready(self) -> None:
        from oit_backend.router import router as main_router
        from valueassessment.urls import router

        main_router.extend(router)
