from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitsSerializer(ModelSerializer):
    """Serializer привычек"""

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        """Валидация проверяющая:
         - выбрал пользователь вознаграждение или приятную привычку, но не оба варианта.
         - что время выполнения должно быть не больше 120 секунд"""

        associated_habit = data.get('associated_habit')
        reward = data.get('reward')
        time_to_complete = data.get('time_to_complete')

        if associated_habit and reward:
            raise serializers.ValidationError("Нельзя выбрать одновременно вознаграждение и приятную привычку")

        if time_to_complete > 120:
            raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")

        return data