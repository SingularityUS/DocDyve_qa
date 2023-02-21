from rest_framework import generics
from .qa import answer_question
from rest_framework.response import Response
from myapp.models import Document, Question
from myapp.serializers import DocumentSerializer, QuestionSerializer

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class AnswerQuestionView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()

    def get(self, request, *args, **kwargs):
        question_id = self.kwargs['pk']
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Question does not exist.'}, status=404)

        # Use the qa.py script to answer the question
        documents = Document.objects.all()
        answers = answer_question(question.text, documents)

        return Response({'answer': answers[0]})
