from django.urls import path, include
import debug_toolbar
from . import views






app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
 # urls.py
    path("question/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('__debug__/', include(debug_toolbar.urls)),
    path("register/", views.register_view, name="register"),
    path("vote/<int:question_id>/", views.vote, name="vote"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

] 