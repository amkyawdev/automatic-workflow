"""
Auth Routes - API Endpoints for Authentication
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import uuid

from src.core.entities.user import User, UserPlan
from src.core.usecases.auth.authenticate_user import AuthenticateUserUseCase
from src.core.usecases.auth.generate_token import GenerateTokenUseCase
from src.presentation.schemas.auth_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse
)
from src.infrastructure.database.postgres_repository import UserRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.utils.config import settings


router = APIRouter()
user_repo = UserRepository()
jwt_handler = JWTHandler()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if email already exists
    existing = await user_repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name,
        hashed_password="",  # Will be hashed in the repository
        plan=UserPlan.FREE
    )
    
    created_user = await user_repo.create(user, user_data.password)
    return UserResponse(**created_user.to_dict())


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    use_case = AuthenticateUserUseCase(user_repo, jwt_handler)
    result = await use_case.execute(form_data.username, form_data.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token, token_data = result
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login/json", response_model=TokenResponse)
async def login_json(credentials: UserLogin):
    """Login with JSON body"""
    use_case = AuthenticateUserUseCase(user_repo, jwt_handler)
    result = await use_case.execute(credentials.email, credentials.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token, token_data = result
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(current_user: User = Depends(get_current_user_from_token)):
    """Refresh access token"""
    access_token = jwt_handler.create_access_token(
        data={"sub": current_user.id}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_from_token)
):
    """Get current user information"""
    return UserResponse(**current_user.to_dict())


async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    user_id = jwt_handler.decode_token(token)
    if user_id is None:
        raise credentials_exception
    
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user
