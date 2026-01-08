from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('quiz/<slug:topic_slug>/', views.start_quiz, name='start_quiz'),
    path('quiz/<slug:topic_slug>/submit/', views.submit_quiz, name='submit_quiz'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('retake-wrong/<int:attempt_id>/', views.retake_wrong, name='retake_wrong'),
]
