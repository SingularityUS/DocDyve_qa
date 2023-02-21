from django.urls import path
from .views import DocumentListCreateView, QuestionListCreateView, AnswerQuestionView

urlpatterns = [
    path('documents/', DocumentListCreateView.as_view(), name='document-list'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list'),
    path('questions/<int:pk>/answer/', AnswerQuestionView.as_view(), name='question-answer'),
]
