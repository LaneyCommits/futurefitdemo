from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.quiz.models import QuizResult

from .serializers import (
    LoginSerializer,
    QuizResultSummarySerializer,
    RegisterSerializer,
    UserSerializer,
)


def _attach_pending_quiz(user, pending_quiz):
    """
    Attach latest anonymous quiz result to user after auth.
    Expects pending_quiz: { "answers": ["q1a", ...] }.
    """
    if not pending_quiz or not isinstance(pending_quiz, dict):
        return
    ordered_answers = pending_quiz.get("answers")
    if not isinstance(ordered_answers, list) or not ordered_answers:
        return

    answers_map = {f"q{i + 1}": key for i, key in enumerate(ordered_answers)}
    anonymous_result = (
        QuizResult.objects.filter(user__isnull=True, answers=answers_map)
        .order_by("-created_at")
        .first()
    )
    if anonymous_result:
        anonymous_result.user = user
        anonymous_result.save(update_fields=["user"])


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """POST /api/users/register/ -- create account and return auth token."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    _attach_pending_quiz(user, serializer.validated_data.get("pending_quiz"))
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "user": UserSerializer(user).data},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """POST /api/users/login/ -- authenticate and return auth token."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)
    _attach_pending_quiz(user, serializer.validated_data.get("pending_quiz"))
    return Response({"token": token.key, "user": UserSerializer(user).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    """GET /api/users/me/ -- return current authenticated user."""
    return Response(UserSerializer(request.user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """GET /api/users/dashboard/ -- latest + history of saved quiz reports."""
    history_qs = (
        QuizResult.objects.filter(user=request.user)
        .select_related("primary_type", "secondary_type")
        .order_by("-created_at")
    )
    latest = history_qs.first()
    return Response({
        "user": UserSerializer(request.user).data,
        "latest": QuizResultSummarySerializer(latest).data if latest else None,
        "history": QuizResultSummarySerializer(history_qs[:20], many=True).data,
    })
