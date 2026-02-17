import time
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.server import router as server_router
from prometheus_client import generate_latest
from routes.payment import router as payment_router
import logging
from logging_loki import LokiQueueHandler
import database
from fastapi.testclient import TestClient
from fastapi.routing import APIRoute
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
from fastapi import Depends, HTTPException, status
from multiprocessing import Queue
from dotenv import load_dotenv
import os
from os import getenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app = FastAPI()

Instrumentator().instrument(app).expose(app)




loki_logs_handler = LokiQueueHandler(
    Queue(-1),
    url=getenv("LOKI_ENDPOINT"),
    tags={"application":"fastapi"},
    version="1"
)

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addHandler(loki_logs_handler)

REQUEST_COUNT = Counter('api_requests_total', 'Total API requests')
REQUEST_LATENCY = Histogram('api_request_latency_seconds', 'API request latency')


for route in app.routes:
    if isinstance(route, APIRoute):
        print(route.path)




def verify_admin_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return payload


@app.route("/metrics")
def get_metrics(user = Depends(verify_admin_user)):
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.route('/api/data')
@REQUEST_LATENCY.time()
def get_data():
    REQUEST_COUNT.inc()


app.include_router(user_router, prefix="/api/users")
app.include_router(server_router, prefix="/api/servers")
app.include_router(payment_router, prefix="/api/process-payment")

origins = ["http://localhost:8000"]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
)



@app.get("/test-connection")
async def test_connection():
    try:
        collections = await database.user_collection.database.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return {"status": "error", "message": str(e)}

