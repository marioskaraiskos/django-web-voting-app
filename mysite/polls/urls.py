from django.urls import path, include
from . import views
import debug_toolbar
from .views import DeleteQuestionView

app_name = "polls"

urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    
    # ex: /polls/5/
    path("question/<int:pk>/", views.DetailView.as_view(), name="detail"),
    
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # User management
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('create/', views.create_question, name='create_question'),

    # Debug toolbar
    path("__debug__/", include(debug_toolbar.urls)),
    # ex: /polls/5/delete/
    path('question/<int:pk>/delete/', DeleteQuestionView.as_view(), name='delete_question'),


]
