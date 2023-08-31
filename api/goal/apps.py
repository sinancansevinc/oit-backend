from django.apps import AppConfig


class GoalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goal'

    def ready(self) -> None:
        from goal.urls import router
        from oit_backend.router import router as main_router

        main_router.extend(router)
