from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def prompting(request):
    task = {
        "message": "Task started!",
        "taskid": "hard coded",
    }
    return Response(task,200)