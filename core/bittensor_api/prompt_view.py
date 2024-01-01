import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def prompting(request):
    #pull data from third party rest api
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    #convert reponse data into json
    users = response.json()
    return Response(users)

@api_view(['GET'])
def getTaskStatus(request,id):
    #pull data from third party rest api
    return Response(id)

@api_view(['GET'])
def getTaskResult(request,id):
    #pull data from third party rest api
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    #convert reponse data into json
    users = response.json()
    return Response(users)