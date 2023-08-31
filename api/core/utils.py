from core.models import User


def is_manager(user) -> bool:
    return User.objects.filter(manager=user).exists()
