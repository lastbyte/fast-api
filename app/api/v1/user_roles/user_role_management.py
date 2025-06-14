from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.common.auth.token import authenticate, get_token
from app.connectors.db.postgres import SessionDep
from app.models.db.user_role import UserRole
from app.models.requests.schema import CreateUserRoleRequest
from app.services import user_role_service
from app.common.logger import Logger

logger = Logger(__name__)

router = APIRouter(tags=["User Roles"])

@router.get("/", description="Get all user roles")
async def get_user_roles(db: SessionDep):
    try:
        user_roles = user_role_service.get_all_user_roles(db=db)
        return JSONResponse(content={"user_roles": [user_role.model_dump() for user_role in user_roles]}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
@authenticate
async def create_user_role(db: SessionDep, request: Request, user_role_request: CreateUserRoleRequest, token = Depends(get_token)):
    try:
        user_role = await user_role_service.create_user_role(db=db, user_role_request=user_role_request)
        return JSONResponse(content=user_role.model_dump(), status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{user_role_id}")
@authenticate
async def get_user_role(db: SessionDep, request: Request, user_role_id: int, token = Depends(get_token)):
    try:
        user_role = await user_role_service.get_user_role(db=db, user_role_id=user_role_id)
        return JSONResponse(content=user_role.model_dump(), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/{user_role_id}")
@authenticate
async def update_user_role(db: SessionDep, request: Request, user_role_id: int, user_role_request: CreateUserRoleRequest, token = Depends(get_token)):
    try:
        user_role = await user_role_service.update_user_role(db=db, user_role_id=user_role_id, user_role_request=user_role_request)
        return JSONResponse(content=user_role.model_dump(), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.delete("/{user_role_id}")
@authenticate
async def delete_user_role(db: SessionDep, request: Request, user_role_id: int, token = Depends(get_token)):
    try:
        await user_role_service.delete_user_role(db=db, user_role_id=user_role_id)
        return JSONResponse(content={"message": "User role deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))