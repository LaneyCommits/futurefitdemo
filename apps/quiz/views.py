from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.quiz.constants import QUIZ_QUESTION_COUNT

from .models import QuizResult
from .serializers import QuestionSerializer, QuizSubmitSerializer
from .services import build_results_payload, calculate_quiz_result, canonical_questions


@api_view(["GET"])
@permission_classes([AllowAny])
def questions_view(request):
    """
    GET /api/quiz/questions/
    Returns exactly 10 questions with choices (no weights exposed).
    """
    questions = canonical_questions()
    if len(questions) != QUIZ_QUESTION_COUNT:
        return Response(
            {
                "error": (
                    f"Quiz must have exactly {QUIZ_QUESTION_COUNT} questions. "
                    "Run: python manage.py seed_careers && python manage.py seed_quiz"
                )
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_view(request):
    """
    POST /api/quiz/submit/
    Body: { "answers": ["q1a", "q2b", ...] }
    Returns personality, explanation, majors, and careers.
    """
    serializer = QuizSubmitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    answers = serializer.validated_data["answers"]
    result = calculate_quiz_result(answers)

    if not result:
        return Response(
            {
                "error": (
                    "Could not score quiz. Submit exactly 10 valid choice keys "
                    "in the same order as /api/quiz/questions/."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    payload = build_results_payload(result)

    primary = result["primary_type"]
    secondary = result["secondary_type"]
    QuizResult.objects.create(
        user=request.user if request.user.is_authenticated else None,
        primary_type=primary,
        secondary_type=secondary,
        answers={f"q{i+1}": key for i, key in enumerate(answers)},
        scores=result["scores"],
    )

    return Response(payload)
