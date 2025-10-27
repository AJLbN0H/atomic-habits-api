from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginations import CustomPagination
from habits.permissions import IsOwner
from habits.serializers import HabitsSerializer


class UserHabitsListAPIView(ListAPIView):
    """Generic вывода списка личных привычек пользователя."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(user_id=self.request.user)


class PublicHabitsListAPIView(ListAPIView):
    """Generic вывода списка публичных привычек пользователей."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()

    def get_queryset(self):
        return Habit.objects.filter(publication_sign=True)


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
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsRetrieveAPIView(RetrieveAPIView):
    """Generic детальной информации о привычке."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsDestroyAPIView(DestroyAPIView):
    """Generic удаленияпривычек пользователя."""

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
