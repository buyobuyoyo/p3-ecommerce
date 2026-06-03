from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

@router.get("/login/github")
def login_github():
    response = supabase.auth.sign_in_with_oauth({
        "provider": "github"
    })
    return {"url": response.url}