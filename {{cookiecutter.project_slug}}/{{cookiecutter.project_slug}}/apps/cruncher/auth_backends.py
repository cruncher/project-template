from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.users.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, email="", username="", password="", **kwargs):
        print(email, username, password, kwargs)
        users = User.objects.filter(Q(email=email) | Q(email=username))
        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return None
