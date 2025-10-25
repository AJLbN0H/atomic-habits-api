from django.db import models

from users.models import User


class Habit(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=500,
        verbose_name="Место",
        help_text="место, в котором необходимо выполнять привычку",
    )
    time = models.DateTimeField(
        verbose_name="Время", help_text="время, когда необходимо выполнять привычку"
    )
    action = models.CharField(
        max_length=500,
        verbose_name="Действие",
        help_text="действие, которое представляет собой привычка",
    )
    a_sign_of_a_pleasant_habit = models.BooleanField(
        verbose_name="Это приятная привычка?",
        help_text="привычка, которую можно привязать к выполнению полезной привычки",
        default=False,
    )
    associated_habit = models.CharField(
        max_length=500,
        verbose_name="Связанная привычка",
        help_text="укажите приятную привычку",
        blank=True,
        null=True,
    )
    periodicity = models.PositiveIntegerField(
        verbose_name="Периодичность",
        help_text="периодичность выполнения привычки для напоминания в днях",
        default=1,
    )
    reward = models.TextField(
        verbose_name="Вознаграждение",
        help_text="введите то, что вы хотели бы получить в виде вознаграждения",
        blank=True,
        null=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время на выполнение",
        help_text="предположительное время, которое вы потратите на выполение привычки",
    )
    publication_sign = models.BooleanField(
        verbose_name="Признак публичности", help_text="опубликовать?", default=False
    )

    def __str__(self):
        return f"Пользователь: {self.user}, Действие: {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
