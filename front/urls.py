from . import views
from django.urls import path


urlpatterns = [
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz_detail')
]