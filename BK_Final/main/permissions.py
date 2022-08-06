from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):    # Создание своего условидя доступа
    def has_permission(self, request, view):            # Проверка авторизации
        if request.method in permissions.SAFE_METHODS:  # Если методы запроса являются безопастными (GET, HEAD, OPTIONS)
            return True

        return bool(request.user and request.user.is_staff) # Для остальных методов у пользователя должен быть флаг is_staff

