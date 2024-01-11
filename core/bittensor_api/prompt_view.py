import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def prompting(request):
    #pull data from third party rest api
    #convert reponse data into json
    return Response({
        'authenticated':True
    })

@api_view(['GET'])
def getTaskStatus(request,id):
    #pull data from third party rest api
    return Response(id)

@api_view(['GET'])
def getTaskResult(request,id):
    #pull data from third party rest api
    response = requests.get('https://7d36-157-97-134-115.ngrok-free.app/')
    #convert reponse data into json
    users = response.json()
    return Response(users)