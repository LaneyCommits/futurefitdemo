from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile
from apps.quiz.models import QuizResult

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    pending_quiz = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["username", "password", "pending_quiz"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        Profile.objects.get_or_create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    pending_quiz = serializers.JSONField(required=False)


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source="profile.bio", read_only=True, default="")

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio"]


class QuizResultSummarySerializer(serializers.ModelSerializer):
    primary_key = serializers.CharField(source="primary_type.key", read_only=True)
    primary_name = serializers.CharField(source="primary_type.name", read_only=True)
    secondary_key = serializers.CharField(source="secondary_type.key", read_only=True)
    secondary_name = serializers.CharField(source="secondary_type.name", read_only=True)

    class Meta:
        model = QuizResult
        fields = [
            "id",
            "created_at",
            "primary_key",
            "primary_name",
            "secondary_key",
            "secondary_name",
            "scores",
            "answers",
        ]
