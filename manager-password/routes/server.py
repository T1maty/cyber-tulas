from fastapi import APIRouter, HTTPException
from models.server import ServerBaseCreate
from models.server import ServerResponse
from database import server_collection
from bson import ObjectId
import logging

router = APIRouter()


logger = logging.getLogger(__name__)

@router.post("/create-server", response_model=ServerBaseCreate)
async def create_server(server: ServerResponse):
    server_dict = server.dict(by_alias=True)
    result = await server_collection.insert_one(server_dict)
    server_dict["_id"] = str(result.inserted_id)
    return server_dict

@router.get("/get-servers", response_model=list[ServerResponse])
async def get_servers(owner_id: str):
    servers = await server_collection.find({"owner_id": ObjectId(owner_id)}).to_list(100)
    return servers


@router.delete("/api/servers/{id}")
async def delete_user(id: str):
    try:
        result = await server_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Server not found")
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "Server successfully deleted"}