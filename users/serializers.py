from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Serializer вывода пользователей."""

    class Meta:
        model = User
        fields = "__all__"
