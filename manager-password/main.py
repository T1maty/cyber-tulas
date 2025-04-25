import time
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from routes.user import router as user_router
import logging
from database import user_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

origins = ["http://localhost","http://localhost:8000"]


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.perf_conter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



app.include_router(user_router, prefix="/api")

@app.get("/test-connection")
async def test_connection():
    try:
        collections = await user_collection.database.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return {"status": "error", "message": str(e)}