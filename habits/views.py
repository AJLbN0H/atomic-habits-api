from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from habits.models import Habit
from habits.paginations import CustomPagination
from habits.serializers import HabitsSerializer


class UserHabitsListAPIView(ListAPIView):
    """Generic вывода списка личных привычек пользователя."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    pagination_class = CustomPagination


class PublicHabitsListAPIView(ListAPIView):
    """Generic вывода списка публичных привычек пользователей."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()


class HabitsCreateAPIView(CreateAPIView):
    """Generic создания привычки."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле user на текущего авторизованного пользователя."""
        serializer.save(user=self.request.user)


class HabitsUpdateAPIView(UpdateAPIView):
    """Generic редактирования привычки."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()


class HabitsRetrieveAPIView(RetrieveAPIView):
    """Generic детальной информации о привычке."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()


class HabitsDestroyAPIView(DestroyAPIView):
    """Generic удаленияпривычек пользователя."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
