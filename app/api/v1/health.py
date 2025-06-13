
from fastapi import APIRouter


router = APIRouter(tags=["Health"]);

@router.get("/health-check")
def health_check(): 
    return { "status" : "OK"}