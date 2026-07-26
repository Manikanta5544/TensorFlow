from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.api.schemas import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from src.auth.application.service import AuthService
from src.auth.domain.entities import User
from src.shared.database.session import get_db
from src.shared.responses.envelope import ok
from src.shared.security.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    user, token = service.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role,
        company_name=payload.company_name,
    )
    return ok(AuthResponse(user=UserResponse.model_validate(user), access_token=token).model_dump())


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    user, token = service.login(email=payload.email, password=payload.password)
    return ok(AuthResponse(user=UserResponse.model_validate(user), access_token=token).model_dump())


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return ok(UserResponse.model_validate(current_user).model_dump())
