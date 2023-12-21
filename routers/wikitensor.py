import os
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Security, BackgroundTasks
from fastapi.security import APIKeyHeader
from starlette.responses import JSONResponse

# from celery_tasks.tasks import get_all_universities_task, get_university_task
from dotenv import load_dotenv
from typing import Literal, Optional, List
from fastapi import FastAPI, WebSocket
import time
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

load_dotenv()

class article_request(BaseModel):
    topic: str
    source: Literal["openai", "bittensor"]
    personal_apikey: Optional[str] = None


router = APIRouter(
    prefix="/wikitensor",
    tags=["Wikitensor"],
    responses={404: {"description": "Not found"}},
)

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in ls_api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@router.get("/protected")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}


# generate_article
@router.post("/api/article")
def get_article(
    article_request: article_request,
    api_key: str = Security(get_api_key),
):
    source = article_request.source
    topic = article_request.topic
    personal_apikey = article_request.personal_apikey
    source = source.lower()
    if source not in ["openai", "bittensor"]:
        raise ValueError(
            f"source: {source} not accepted. Only 'openai' or 'bittensor' accepted."
        )
    # check if we already have a article generated we can return
  
    # FIX TO LOOK FOR OPENAI SPECIFIC
    response = {"data":{"source":"bittensor"}}
    if not response.data:
        new_article_id = 'article_id'
        # determine what task to start
        if source == "openai":
            task = openai_generate_new_article.apply_async(args=[topic, new_article_id])

        elif source == "bittensor":
           print("celery removed")
        return {
            "message": "Task started! Check for the article at the article_id",
            "article_id": new_article_id,
            "taskid": "validator_task.id",
        }
    else:
        return {
            "message": "Article already exists, see article_id",
            "article_id": response.data,
        }


@router.get("/api/article_status/{article_id}")
def get_article_id_status(article_id: int, api_key: str = Security(get_api_key)):
    return article_id


@router.get("/task/status/{task_id}")
async def get_task_status(task_id: str, api_key: str = Security(get_api_key)) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)


@router.get("/task/result/{task_id}")
async def get_task_result(task_id: str, api_key: str = Security(get_api_key)):
    """
    Get the result of a Celery task using its task ID.
    """
    result = AsyncResult(task_id)
    if result.successful():
        return JSONResponse({"result": result.result})
    elif result.failed():
        return JSONResponse(
            {"error": "Task execution failed", "traceback": result.traceback},
            status_code=500,
        )
    else:
        return JSONResponse(
            {"status": "Task is still pending or in progress"}, status_code=202
        )


# Dictionary to store WebSocket connections for each task_id


def generate_article_from_task_update(update, title):
    article = f"{title}\n\n"
    for section in update:
        article += section["Section Title"] + "\n\n"
        article += section["Response"] + "\n\n\n"
    return article
