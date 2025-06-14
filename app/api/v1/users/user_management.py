
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.common.auth.token import authenticate, create_auth_token, get_token, verify_token
from app.connectors.db.postgres import SessionDep
from app.exceptions.database_exceptions import EntityExists
from app.models.requests.create_user_request import CreateUserRequest, LoginRequest
from app.models.responses.users import InvalidUserRequest
from app.models.db.user import User
from app.services import user_service
from app.common.logger import Logger


router = APIRouter(tags=["User"])
logger = Logger(__name__)


@router.post("/sign-up", responses={"200": {"model": User}, "400": {"model":  InvalidUserRequest}})
async def sign_up(create_user_request: CreateUserRequest,db: SessionDep):
    try:
        user = await user_service.create_user(db=db, create_user_request=create_user_request)
        token = create_auth_token(user=user)
        return JSONResponse(content={"user": user.model_dump(), "token": token}, status_code=200)
    
    except EntityExists:
        logger.error(
            f"user account already exists for the email id {create_user_request.email}")
        return JSONResponse(content={"errors" : f'user account already exists for the email id {create_user_request.email}'}, status_code=400)

    except Exception as ex:
        logger.error(f"error occurred while adding user {str(ex)}")

@router.post("/login", description="Generate JWT token using email and password")
async def login(login_request: LoginRequest, db: SessionDep):
    try:
        user = await user_service.login_user(db=db,login_request=login_request)
        token = create_auth_token(user=user)
        return JSONResponse(content={"token": token}, status_code=200)
    except Exception as ex:
        logger.error(f"error occurred while adding user :  {str(ex)}")

@router.get("/logout", description="invalidates the jwt token")
async def logout(token = Depends(get_token)):
    try:
        is_successful = await user_service.logout(token=token)
        return JSONResponse(content={"success": is_successful}, status_code=200)
    except Exception as ex:
        logger.error(f"error occurred while adding user :  {str(ex)}")


@router.get("/search", description="Search users by name for email")
@authenticate
async def search(db: SessionDep,
                 request : Request,
                 token = Depends(verify_token),
                 q: str | None = "",
                 page_size: int | None = 10,
                 page_num: int | None = 1,
                 sort_dir: str | None = "asc",
                 sort_column: str | None = "id"):
    try:
        total, users = await user_service.list_users(
            db=db, q=q, sort_dir=sort_dir, sort_column=sort_column, page_num=page_num, page_size=page_size)
        return JSONResponse(
            content={
                "results": users,
                "page_num": page_num,
                "page_size": page_size,
                "total_pages": (total//page_size) + 1
            },
            status_code=200
        )
    except Exception as ex:
        logger.error("Error occurred while fetching the user list")


@router.get("/profile/me")
@authenticate
async def search(db: SessionDep,request: Request, token = Depends(verify_token)):
    try:
        user_data = await user_service.get_user(db=db, user_id=request.state.user["id"])
        return JSONResponse(
            content=user_data.model_dump(),
            status_code=200
        )
    except Exception as ex:
        logger.error(f"Error occurred while fetching user")
