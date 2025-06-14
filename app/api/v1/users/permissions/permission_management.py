from fastapi import APIRouter

router = APIRouter(tags=["Permissions"])

@router.get("")
async def get_permissions():
    return {"message": "Hello, World!"}


@router.post("")
async def create_permission():
    return {"message": "Hello, World!"}


@router.get("/{permission_id}")
async def get_permission(permission_id: int):
    return {"message": "Hello, World!"}


@router.put("/{permission_id}")
async def update_permission(permission_id: int):
    return {"message": "Hello, World!"}

@router.delete("/{permission_id}")
async def delete_permission(permission_id: int):
    return {"message": "Hello, World!"}

