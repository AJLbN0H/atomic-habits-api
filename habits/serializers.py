from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitsSerializer(ModelSerializer):
    """Serializer привычек"""

    class Meta:
        model = Habit
        fields = "__all__"
