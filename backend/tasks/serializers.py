from rest_framework import serializers
from dateutil import parser

class TaskSerializer(serializers.Serializer):
    """
    Serializer validates each task sent to the API.
    Helps us enforce required structure before scoring.
    """

    id = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(max_length=255)
    due_date = serializers.CharField(required=False, allow_blank=True)
    estimated_hours = serializers.FloatField(required=False, default=1.0)
    importance = serializers.IntegerField(required=False, default=5, min_value=1, max_value=10)
    dependencies = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )

    def validate_due_date(self, value):
        """
        Validate date format only if provided.
        Accepts ISO strings: YYYY-MM-DD
        """
        if not value:
            return None

        try:
            parser.parse(value)
        except:
            raise serializers.ValidationError("Invalid date format.")

        return value
