from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8')[:72],
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    """Generate a bcrypt password hash, truncated to 72 bytes safely"""
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


from google import genai
from fastapi import HTTPException, status
from app.core.config import settings
from app.prompts.email_analysis import EMAIL_ANALYSIS_SYSTEM_PROMPT, get_email_analysis_prompt
from app.schemas.analysis import EmailAnalysis

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def analyze_email_content(sender: str, subject: str, body: str) -> EmailAnalysis:
    user_prompt = get_email_analysis_prompt(sender, subject, body)
    full_prompt = f"{EMAIL_ANALYSIS_SYSTEM_PROMPT}\n\n{user_prompt}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        
        analysis_result = EmailAnalysis.model_validate_json(response.text)
        return analysis_result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service temporarily unavailable or invalid response: {str(e)}"
        )