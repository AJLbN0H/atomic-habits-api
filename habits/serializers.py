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
         - выбрал пользователь вознаграждение или приятную привычку, но не оба варианта
         - время выполнения должно быть не больше 120 секунд
         - в связанные привычки могут попадать только привычки с признаком приятной привычки
         - у приятной привычки не может быть вознаграждения или связанной привычки
         - нельзя выполнять привычку реже, чем 1 раз в 7 дней."""

        associated_habit = data.get('associated_habit')
        reward = data.get('reward')
        time_to_complete = data.get('time_to_complete')
        a_sign_of_a_pleasant_habit = data.get('a_sign_of_a_pleasant_habit')
        periodicity = data.get('periodicity')

        if associated_habit and reward:
            raise serializers.ValidationError("Нельзя выбрать одновременно вознаграждение и приятную привычку")

        if time_to_complete > 120:
            raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")

        if not associated_habit.a_sign_of_a_pleasant_habit:
            raise serializers.ValidationError("Привычка, которую вы выбрали не является приятной")

        if a_sign_of_a_pleasant_habit:
            if associated_habit or reward:
                raise serializers.ValidationError("Для приятной привычки нельзя выбрать вознаграждение или еще одну приятную привычку")

        if periodicity < 1:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней")

        return data