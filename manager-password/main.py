import time
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.server import router as server_router
import logging
from database import user_collection
from fastapi.testclient import TestClient
from fastapi.routing import APIRoute
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app = FastAPI()



for route in app.routes:
    if isinstance(route, APIRoute):
        print(route.path)



app.include_router(user_router, prefix="/api/users")
app.include_router(server_router, prefix="/api/servers")

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
        collections = await user_collection.database.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return {"status": "error", "message": str(e)}