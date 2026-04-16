from rest_framework import serializers

from apps.quiz.constants import QUIZ_QUESTION_COUNT
from apps.quiz.models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["key", "label", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "order", "choices"]


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.CharField(max_length=16),
        min_length=QUIZ_QUESTION_COUNT,
        max_length=QUIZ_QUESTION_COUNT,
        help_text=f"Exactly {QUIZ_QUESTION_COUNT} choice keys in question order.",
    )

    def validate_answers(self, value):
        if len(value) != QUIZ_QUESTION_COUNT:
            raise serializers.ValidationError(
                f"Must submit exactly {QUIZ_QUESTION_COUNT} answers."
            )
        questions = list(
            Question.objects.order_by("order")[:QUIZ_QUESTION_COUNT]
        )
        if len(questions) != QUIZ_QUESTION_COUNT:
            raise serializers.ValidationError("Quiz is not configured correctly.")
        for i, key in enumerate(value):
            if not Choice.objects.filter(question=questions[i], key=key).exists():
                raise serializers.ValidationError(
                    f"Invalid choice for question position {i + 1}."
                )
        return value
