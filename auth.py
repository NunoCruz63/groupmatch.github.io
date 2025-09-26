from fastapi import HTTPException, Request, Cookie, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Annotated
import httpx
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import User, SessionData
import logging

logger = logging.getLogger(__name__)

class EmergentAuth:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.session_url = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"
        
    async def get_session_data(self, session_id: str) -> Optional[SessionData]:
        """Get user session data from Emergent Auth"""
        try:
            headers = {"X-Session-ID": session_id}
            async with httpx.AsyncClient() as client:
                response = await client.get(self.session_url, headers=headers)
                
            if response.status_code == 200:
                data = response.json()
                return SessionData(**data)
            else:
                logger.warning(f"Failed to get session data: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting session data: {str(e)}")
            return None
    
    async def create_or_update_user(self, session_data: SessionData) -> User:
        """Create or update user in database"""
        try:
            # Check if user exists
            existing_user = await self.db.users.find_one({"email": session_data.email})
            
            if existing_user:
                # Update existing user
                update_data = {
                    "session_token": session_data.session_token,
                    "session_expires": datetime.now(timezone.utc) + timedelta(days=7),
                    "lastLogin": datetime.now(timezone.utc),
                    "name": session_data.name,
                    "picture": session_data.picture
                }
                
                await self.db.users.update_one(
                    {"email": session_data.email},
                    {"$set": update_data}
                )
                
                # Get updated user
                updated_user = await self.db.users.find_one({"email": session_data.email})
                return User(**updated_user)
            else:
                # Create new user
                new_user = User(
                    id=session_data.id,
                    email=session_data.email,
                    name=session_data.name,
                    picture=session_data.picture,
                    session_token=session_data.session_token,
                    session_expires=datetime.now(timezone.utc) + timedelta(days=7),
                    is_admin=False,  # You can manually set admin users in the database
                    lastLogin=datetime.now(timezone.utc)
                )
                
                await self.db.users.insert_one(new_user.dict())
                return new_user
                
        except Exception as e:
            logger.error(f"Error creating/updating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to process user data")
    
    async def get_current_user(self, 
                             request: Request,
                             session_token: Annotated[Optional[str], Cookie(alias="session_token")] = None,
                             authorization: Optional[str] = None) -> Optional[User]:
        """Get current authenticated user from session token"""
        try:
            # Try cookie first, then Authorization header
            token = session_token
            if not token and authorization:
                if authorization.startswith("Bearer "):
                    token = authorization[7:]
                else:
                    token = authorization
            
            if not token:
                return None
            
            # Find user by session token
            user_data = await self.db.users.find_one({
                "session_token": token,
                "session_expires": {"$gt": datetime.now(timezone.utc)}
            })
            
            if user_data:
                return User(**user_data)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            return None
    
    async def require_auth(self, 
                         request: Request,
                         session_token: Annotated[Optional[str], Cookie(alias="session_token")] = None,
                         authorization: Optional[str] = None) -> User:
        """Require authentication - raises 401 if not authenticated"""
        user = await self.get_current_user(request, session_token, authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")
        return user
    
    async def require_admin(self, 
                          request: Request,
                          session_token: Annotated[Optional[str], Cookie(alias="session_token")] = None,
                          authorization: Optional[str] = None) -> User:
        """Require admin authentication"""
        user = await self.require_auth(request, session_token, authorization)
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        return user
    
    async def logout_user(self, user_id: str):
        """Logout user by removing session token"""
        try:
            await self.db.users.update_one(
                {"id": user_id},
                {"$unset": {"session_token": "", "session_expires": ""}}
            )
        except Exception as e:
            logger.error(f"Error logging out user: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to logout")