from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def authroize(request):
    #pull data from third party rest api
    complete_url = request.query_params.get("id_token")
    return Response({"token":complete_url})