from rest_framework import serializers

from .models import Job, Major, PersonalityType


class PersonalityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityType
        fields = ["key", "name", "description", "icon"]


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ["key", "name", "description"]


class JobSerializer(serializers.ModelSerializer):
    primary_archetype = serializers.SlugRelatedField(
        slug_field="key", read_only=True
    )

    class Meta:
        model = Job
        fields = ["id", "title", "description", "learn_more", "primary_archetype"]


class RecommendationSerializer(serializers.Serializer):
    """Read-only serializer for the /recommendations/ endpoint response."""

    personality = serializers.DictField(read_only=True)
    majors = MajorSerializer(many=True, read_only=True)
    jobs = JobSerializer(many=True, read_only=True)
