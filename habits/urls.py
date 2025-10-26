
from django.urls import path

from habits.views import UserHabitsListAPIView, PublicHabitsListAPIView, HabitsCreateAPIView, HabitsUpdateAPIView, \
    HabitsRetrieveAPIView, HabitsDestroyAPIView

app_name = "habits"

urlpatterns = [
    path('public/', UserHabitsListAPIView.as_view(), name='habits_public_list'),
    path('', PublicHabitsListAPIView.as_view(), name='habits_list'),
    path('create/', HabitsCreateAPIView.as_view(), name='habits_create'),
    path('update/', HabitsUpdateAPIView.as_view(), name='habits_update'),
    path('detail/', HabitsRetrieveAPIView.as_view(), name='habits_detail'),
    path('delete/', HabitsDestroyAPIView.as_view(), name='habits_delete'),
]
