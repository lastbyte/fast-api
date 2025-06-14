from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from app.common.auth.token import authenticate, get_token, validate_permissions
from app.connectors.db.postgres import SessionDep
from app.exceptions.database_exceptions import DbException
from app.models.requests.schema import UserPermissionCreateRequest, UserPermissionUpdateRequest
from app.models.responses.schema import UserPermissionCreateResponse, UserPermissionDeleteResponse, UserPermissionListResponse, UserPermissionUpdateResponse
from app.services import user_permission_service

router = APIRouter(tags=["Permissions"])

@router.get("")
@authenticate
@validate_permissions(allowed_permissions=[1])
async def get_permissions(db: SessionDep, request: Request, token = Depends(get_token), page_num: int = 1, page_size: int = 10):
    try:
        permissions, total_count = await user_permission_service.get_all_permissions(db=db, page_num=page_num, page_size=page_size)
        return JSONResponse(content=UserPermissionListResponse(permissions=permissions, total_count=total_count, page_size=page_size, page_num=page_num).model_dump(), status_code=200)
    except DbException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
@authenticate
@validate_permissions(allowed_permissions=[1])
async def create_permission(db: SessionDep, request: Request, token = Depends(get_token), create_permission_request: UserPermissionCreateRequest = Body(...)):
    try:
        permission = await user_permission_service.create_permission(db=db, permission=create_permission_request)
        return JSONResponse(content=UserPermissionCreateResponse(permission=permission).model_dump(), status_code=200)
    except DbException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{permission_id}")
@authenticate
@validate_permissions(allowed_permissions=[1])
async def get_permission(db: SessionDep, request: Request, permission_id: int, token = Depends(get_token)):
    try:
        permission = await user_permission_service.get_permission_by_id(db=db, permission_id=permission_id)
        return JSONResponse(content=UserPermissionUpdateResponse(permission=permission).model_dump(), status_code=200)
    except DbException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{permission_id}")
@authenticate
@validate_permissions(allowed_permissions=[1])
async def update_permission(db: SessionDep, request: Request, permission_id: int, token = Depends(get_token), update_permission_request: UserPermissionUpdateRequest = Body(...)):
    try:
        permission = await user_permission_service.update_permission(db=db, permission_id=permission_id, permission=update_permission_request)
        return JSONResponse(content=UserPermissionUpdateResponse(permission=permission).model_dump(), status_code=200)
    except DbException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{permission_id}")
@authenticate
@validate_permissions(allowed_permissions=[1])
async def delete_permission(db: SessionDep, request: Request, permission_id: int, token = Depends(get_token)):
    try:
        await user_permission_service.delete_permission(db=db, permission_id=permission_id)
        return JSONResponse(content=UserPermissionDeleteResponse(success=True).model_dump(), status_code=200)
    except DbException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))