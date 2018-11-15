from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class EmailBackend(object):
    def authenticate(self, email="", password=""):
        users = User.objects.filter(email=email)
        for user in users:
            if user.is_active and check_password(password, user.password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
