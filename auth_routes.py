from fastapi import APIRouter, HTTPException, Response, Request, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Annotated
from auth import EmergentAuth
from models import User, SessionData
from database import database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Initialize auth instance
auth = EmergentAuth(database.db)

@router.post("/session")
async def process_session(request: Request):
    """Process session ID from Emergent Auth and create session"""
    try:
        body = await request.json()
        session_id = body.get("session_id")
        
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id required")
        
        # Get session data from Emergent
        session_data = await auth.get_session_data(session_id)
        if not session_data:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        # Create or update user
        user = await auth.create_or_update_user(session_data)
        
        # Create response with cookie
        response_data = {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "picture": user.picture,
                "is_admin": user.is_admin
            }
        }
        
        response = JSONResponse(content=response_data)
        
        # Set httpOnly cookie
        response.set_cookie(
            key="session_token",
            value=session_data.session_token,
            max_age=7 * 24 * 60 * 60,  # 7 days
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process session")

@router.get("/me")
async def get_current_user_info(request: Request):
    """Get current authenticated user information"""
    try:
        user = await auth.get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "picture": user.picture,
                "is_admin": user.is_admin,
                "lastLogin": user.lastLogin
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user info")

@router.post("/logout")
async def logout(request: Request):
    """Logout current user"""
    try:
        user = await auth.get_current_user(request)
        if user:
            await auth.logout_user(user.id)
        
        response = JSONResponse(content={"success": True, "message": "Logged out successfully"})
        
        # Clear cookie
        response.delete_cookie(
            key="session_token",
            path="/",
            secure=True,
            samesite="none"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to logout")

@router.get("/check")
async def check_auth_status(request: Request):
    """Check if user is authenticated"""
    try:
        user = await auth.get_current_user(request)
        
        return {
            "authenticated": user is not None,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "picture": user.picture,
                "is_admin": user.is_admin
            } if user else None
        }
        
    except Exception as e:
        logger.error(f"Error checking auth status: {str(e)}")
        return {"authenticated": False, "user": None}