
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse

from app.common.auth.token import authenticate, create_auth_token, get_token, validate_permissions, verify_token
from app.connectors.db.postgres import SessionDep
from app.exceptions.database_exceptions import DbException
from app.models.requests.schema import CreateUserRequest, LoginRequest, UpdatePasswordRequest, UpdateUserProfileRequest
from app.models.responses.schema import SelfUserProfileResponse, UserProfileResponse
from app.models.db.schema import User
from app.services import user_profile_service, user_service
from app.common.logger import Logger


router = APIRouter()
logger = Logger(__name__)


@router.post("/sign-up", responses={"200": {"model": User}}, tags=["Authentication"])
async def sign_up(db: SessionDep, create_user_request: CreateUserRequest = Body(...)):
    try:
        user = await user_service.create_user(db=db, create_user_request=create_user_request)
        token = create_auth_token(user=user)
        return JSONResponse(content={"user": user.model_dump(), "token": token}, status_code=200)
    
    except DbException:
        logger.error(
            f"user account already exists for the email id {create_user_request.email}")
        return JSONResponse(content={"errors" : f'user account already exists for the email id {create_user_request.email}'}, status_code=400)

    except Exception as ex:
        logger.error(f"error occurred while adding user {str(ex)}")

@router.post("/login", description="Generate JWT token using email and password", tags=["Authentication"])
async def login(db: SessionDep, login_request: LoginRequest = Body(...)):
    try:
        user = await user_service.login_user(db=db,login_request=login_request)
        token = create_auth_token(user=user)
        return JSONResponse(content={"token": token}, status_code=200)
    except Exception as ex:
        logger.error(f"error occurred while adding user :  {str(ex)}")

@router.post("/update/password", tags=["Authentication"])
@authenticate
async def update_password(db: SessionDep, request: Request, update_password_request: UpdatePasswordRequest = Body(...), token = Depends(get_token)):
    try:
        user = await user_service.update_password(db=db, user_id=request.state.user["id"], update_password_request=update_password_request)
        return JSONResponse(content={"user": user.model_dump()}, status_code=200)
    except Exception as ex:
        logger.error(f"error occurred while updating password :  {str(ex)}")

@router.get("/logout", description="invalidates the jwt token", tags=["Authentication"])
async def logout(token = Depends(get_token)):
    try:
        is_successful = await user_service.logout(token=token)
        return JSONResponse(content={"success": is_successful}, status_code=200)
    except Exception as ex:
        logger.error(f"error occurred while adding user :  {str(ex)}")


@router.get("/search", description="Search users by name for email", tags=["Users"])
@authenticate
async def search_users(db: SessionDep,
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


@router.get("/profile/me", responses={"200": {"model": SelfUserProfileResponse}}, tags=["Users"])
@authenticate
async def get_self_user_profile(db: SessionDep,request: Request, token = Depends(verify_token)):
    try:
        user_data = await user_service.get_user(db=db, user_id=request.state.user["id"])

        try:
            user_profile = await user_profile_service.get_user_profile(db=db, user_id=request.state.user["id"])
            return JSONResponse(
                content=SelfUserProfileResponse(user=user_data, profile=user_profile).model_dump(),
                status_code=200
            )
        except DbException as ex:
            logger.error(f"Error occurred while fetching user profile, {str(ex)}")

        return JSONResponse(
            content=SelfUserProfileResponse(user=user_data).model_dump(),
            status_code=200
        )
    except DbException as ex:
        logger.error(f"Error occurred while fetching user profile, {str(ex)}")
    except Exception as ex:
        logger.error(f"Error occurred while fetching user, {str(ex)}")


@router.get("/profile/{user_id}", responses={"200": {"model": UserProfileResponse}}, tags=["User Profile"])
@authenticate
async def get_user_profile(db: SessionDep,user_id: int,request: Request, token = Depends(verify_token)):
    try:
        user_profile = await user_profile_service.get_user_profile(db=db, user_id=user_id)
        return JSONResponse(
            content=UserProfileResponse(profile=user_profile).model_dump(),
            status_code=200
        )
    except Exception as ex:
        logger.error(f"Error occurred while fetching user")
        raise ex

@router.patch("/{user_id}/update/role/{role_id}", tags=["Roles"])
@authenticate
@validate_permissions(allowed_permissions=[1])
async def update_user_role(db: SessionDep, request: Request, user_id: int, role_id: int, token = Depends(get_token)):
    try:
        user_data = await user_service.update_user_role(db=db, user_id=user_id, role_id=role_id)
        return JSONResponse(
            content=user_data.model_dump(),
            status_code=200
        )
    except Exception as ex:
        logger.error(f"Error occurred while fetching user")


@router.patch("/update/profile", responses={"200": {"model": SelfUserProfileResponse}}, tags=["User Profile"])
@authenticate
async def update_self_user_profile(db: SessionDep, request: Request, user_profile_request: UpdateUserProfileRequest, token = Depends(get_token)):
    try:
        user_profile = await user_profile_service.update_user_profile(db=db, user_id=request.state.user["id"], user_profile_request=user_profile_request)
        return JSONResponse(
            content=user_profile.model_dump(),
            status_code=200
        )
    except Exception as ex:
        logger.error(f"Error occurred while fetching user")
        raise ex
    

@router.patch("/{user_id}/update/profile", responses={"200": {"model": SelfUserProfileResponse}}, tags=["User Profile"])
@authenticate
async def update_user_profile(db: SessionDep, request: Request, user_id: int, user_profile_request: UpdateUserProfileRequest, token = Depends(get_token)):
    try:
        user_profile = await user_profile_service.update_user_profile(db=db, user_id=user_id, user_profile_request=user_profile_request)
        return JSONResponse(
            content=user_profile.model_dump(),
            status_code=200
        )
    except Exception as ex:
        logger.error(f"Error occurred while fetching user")
        raise ex


@router.post("/sign-up/verify", responses={"200": {"model": User}}, tags=["Authentication"])
async def verify_user_sign_up(db: SessionDep, user_id: int, verification_code: str):
    try:
        user = await user_service.verify_user_sign_up(db=db, user_id=user_id, verification_code=verification_code)
        return JSONResponse(content=user.model_dump(), status_code=200)
    except Exception as ex:
        logger.error(f"Error occurred while verifying user")
        raise ex