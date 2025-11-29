#views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .scoring import analyze

class AnalyzeTasks(APIView):
    """
    POST /api/tasks/analyze/
    Accepts task list + strategy, returns sorted results.
    """

    def post(self, request):
        tasks = request.data.get("tasks", [])
        strategy = request.data.get("strategy", "smart")

        valid = []
        errors = []

        for i, task in enumerate(tasks):
            serializer = TaskSerializer(data=task)
            if serializer.is_valid():
                obj = serializer.validated_data
                obj["id"] = obj.get("id") or obj["title"]
                valid.append(obj)
            else:
                errors.append({"index": i, "errors": serializer.errors})

        if errors:
            return Response({"validation_errors": errors}, status=400)

        result = analyze(valid, strategy)
        return Response(result)


class SuggestTasks(APIView):
    """
    POST /api/tasks/suggest/
    Returns only the top 3 recommended tasks,
    useful for showing a "what should I do now?" feature.
    """

    def post(self, request):
        tasks = request.data.get("tasks", [])
        strategy = request.data.get("strategy", "smart")

        valid = []
        for t in tasks:
            s = TaskSerializer(data=t)
            if s.is_valid():
                d = s.validated_data
                d["id"] = d.get("id") or d["title"]
                valid.append(d)

        analysis = analyze(valid, strategy)
        top3 = analysis["results"][:3]

        return Response({
            "has_cycle": analysis["has_cycle"],
            "suggestions": top3
        })
