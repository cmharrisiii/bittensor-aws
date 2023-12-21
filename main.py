import time

import uvicorn as uvicorn
from fastapi import FastAPI
from routers import wikitensor
from routers import prompting
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


def create_app() -> FastAPI:
    current_app = FastAPI(
        title="Asynchronous tasks processing with Celery and RabbitMQ",
        description="Sample FastAPI Application to demonstrate Event "
        "driven architecture with Celery and RabbitMQ",
        version="1.0.0",
    )

    current_app.include_router(wikitensor.router)
    current_app.include_router(prompting.router)
    return current_app


origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://wikitensor.com",
    "https://wikitensor.com",
    "https://starfish-app-a89lj.ondigitalocean.app",
    # # Add any other allowed origins here
    "*",  # Allow all origins
]

app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify HTTP methods (e.g., ["GET", "POST"]) here
    allow_headers=["*"],  # You can specify allowed headers here
)
app.add_middleware(HTTPSRedirectMiddleware)


@app.middleware("https")
async def add_process_time_header(request, call_next):
    print("inside middleware!")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:0.4f} sec")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
