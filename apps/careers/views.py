from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Job, Major, PersonalityType
from .serializers import JobSerializer, MajorSerializer, PersonalityTypeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def types_view(request):
    """GET /api/careers/types/ -- list all personality types."""
    types = PersonalityType.objects.all()
    serializer = PersonalityTypeSerializer(types, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def recommendations_view(request):
    """
    GET /api/careers/recommendations/?type=builder
    Returns the personality type with its recommended majors and jobs.
    """
    type_key = request.query_params.get("type", "")
    if not type_key:
        return Response(
            {"error": "Query parameter 'type' is required."},
            status=400,
        )

    personality = PersonalityType.objects.filter(key=type_key).first()
    if not personality:
        return Response({"error": f"Unknown type: {type_key}"}, status=404)

    majors = Major.objects.filter(
        jobs__primary_archetype=personality
    ).distinct()
    jobs = Job.objects.filter(primary_archetype=personality).distinct()

    return Response(
        {
            "personality": PersonalityTypeSerializer(personality).data,
            "majors": MajorSerializer(majors, many=True).data,
            "jobs": JobSerializer(jobs, many=True).data,
        }
    )
