from django.urls import path

from habits.views import (
    UserHabitsListAPIView,
    PublicHabitsListAPIView,
    HabitsCreateAPIView,
    HabitsUpdateAPIView,
    HabitsRetrieveAPIView,
    HabitsDestroyAPIView,
)

app_name = "habits"

urlpatterns = [
    path("user/", UserHabitsListAPIView.as_view(), name="habits_user_list"),
    path("public/", PublicHabitsListAPIView.as_view(), name="habits_public_list"),
    path("create/", HabitsCreateAPIView.as_view(), name="habits_create"),
    path("update/<int:pk>/", HabitsUpdateAPIView.as_view(), name="habits_update"),
    path("detail/<int:pk>/", HabitsRetrieveAPIView.as_view(), name="habits_detail"),
    path("delete/<int:pk>/", HabitsDestroyAPIView.as_view(), name="habits_delete"),
]
