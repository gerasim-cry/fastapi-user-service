from fastapi import Depends, HTTPException, status
from app.auth import get_current_user
from app.schemas import UserRead


def require_admin(current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user