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

router = APIRouter(
    prefix="/prompting",
    tags=["Prompting"],
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


@router.get("/prompt")
def protected_route(
    system_message: str = "",
    prompt: str = "Hello World!",
    optional_netuid: Optional[str] = "",
    timeout: str = "12",
    api_key: str = Security(get_api_key),
):
    return {
        "message": "Task started!",
        "taskid": "hard coded",
    }


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
