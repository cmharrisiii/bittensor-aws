from django.urls import path
from bittensor_api import prompt_view
from bittensor_api import wikitensor_view
from bittensor_api import authorize_view
authorizeUrl = [
    path('/authorize',authorize_view.authroize)
]

propmptingUrl = [
    path('/prompting/prompt',prompt_view.prompting),
    path('/prompting/task/status/<int:id>',prompt_view.getTaskStatus),
    path('/prompting/task/result/<int:id>',prompt_view.getTaskResult)
]
wikitensorUrl = [
    path('/wikitensor/article',wikitensor_view.getArtical),
    path('/wikitensor/article/status/<int:id>',wikitensor_view.getArticalStatus),
    path('/wikitensor/task/status/<int:id>',wikitensor_view.getTaskStatus),
    path('/wikitensor/task/result/<int:id>',wikitensor_view.getTaskResult)
]

urlpatterns = propmptingUrl + wikitensorUrl + authorizeUrl