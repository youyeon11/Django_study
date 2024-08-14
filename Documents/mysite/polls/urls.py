from django.urls import path
from . import views


app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),  # /polls/로 접속할 때 views.index 호출
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, naem = "vote"),
]
