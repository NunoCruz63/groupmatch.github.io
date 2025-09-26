from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import List, Optional
from models import Provider, ProviderCreate, ProviderUpdate, ProviderListResponse, ProviderResponse
from database import database
from auth import EmergentAuth
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/providers", tags=["providers"])

# Initialize auth instance  
auth = EmergentAuth(database.db)

@router.get("/", response_model=ProviderListResponse)
async def get_providers(
    signalType: Optional[str] = Query(None, description="Filter by signal type"),
    riskLevel: Optional[str] = Query(None, description="Filter by risk level"), 
    priceRange: Optional[str] = Query(None, description="Filter by price range"),
    search: Optional[str] = Query(None, description="Search in name and signal types"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """Get all providers with optional filters"""
    try:
        # Build filter query
        filter_query = {}
        
        # Signal type filter
        if signalType and signalType != "all":
            filter_query["signalTypes"] = signalType
        
        # Risk level filter
        if riskLevel and riskLevel != "all":
            filter_query["riskLevel"] = {"$regex": riskLevel, "$options": "i"}
        
        # Price range filter
        if priceRange and priceRange != "all":
            if "-" in priceRange:
                min_price, max_price = map(int, priceRange.split("-"))
                if max_price == 9999:  # Handle "150+" case
                    filter_query["subscriptionPrice"] = {"$gte": min_price}
                else:
                    filter_query["subscriptionPrice"] = {"$gte": min_price, "$lte": max_price}
        
        # Search filter
        if search:
            search_regex = {"$regex": search, "$options": "i"}
            filter_query["$or"] = [
                {"name": search_regex},
                {"signalTypes": {"$elemMatch": search_regex}}
            ]
        
        # Get total count
        total = await database.db.providers.count_documents(filter_query)
        
        # Get providers with pagination
        cursor = database.db.providers.find(filter_query).skip(skip).limit(limit)
        providers_data = await cursor.to_list(length=limit)
        
        providers = [Provider(**provider_data) for provider_data in providers_data]
        
        return ProviderListResponse(
            success=True,
            data=providers,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Error getting providers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get providers")

@router.get("/search")
async def search_providers(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=50)
):
    """Search providers by name or signal types"""
    try:
        search_regex = {"$regex": q, "$options": "i"}
        filter_query = {
            "$or": [
                {"name": search_regex},
                {"signalTypes": {"$elemMatch": search_regex}}
            ]
        }
        
        cursor = database.db.providers.find(filter_query).limit(limit)
        providers_data = await cursor.to_list(length=limit)
        
        providers = [Provider(**provider_data) for provider_data in providers_data]
        
        return ProviderListResponse(
            success=True,
            data=providers,
            total=len(providers)
        )
        
    except Exception as e:
        logger.error(f"Error searching providers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search providers")

@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(provider_id: str):
    """Get single provider by ID"""
    try:
        provider_data = await database.db.providers.find_one({"id": provider_id})
        
        if not provider_data:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        provider = Provider(**provider_data)
        
        return ProviderResponse(
            success=True,
            data=provider
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting provider: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get provider")

@router.post("/", response_model=ProviderResponse)
async def create_provider(
    provider_data: ProviderCreate,
    request: Request
):
    """Create new provider (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Create new provider
        new_provider = Provider(
            id=str(uuid.uuid4()),
            **provider_data.dict(),
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        
        # Insert into database
        await database.db.providers.insert_one(new_provider.dict())
        
        return ProviderResponse(
            success=True,
            data=new_provider,
            message="Provider created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating provider: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create provider")

@router.put("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: str,
    provider_update: ProviderUpdate,
    request: Request
):
    """Update provider (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if provider exists
        existing_provider = await database.db.providers.find_one({"id": provider_id})
        if not existing_provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Prepare update data
        update_data = provider_update.dict(exclude_unset=True)
        if update_data:
            update_data["updatedAt"] = datetime.now(timezone.utc)
            
            # Update provider
            await database.db.providers.update_one(
                {"id": provider_id},
                {"$set": update_data}
            )
        
        # Get updated provider
        updated_provider_data = await database.db.providers.find_one({"id": provider_id})
        updated_provider = Provider(**updated_provider_data)
        
        return ProviderResponse(
            success=True,
            data=updated_provider,
            message="Provider updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating provider: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update provider")

@router.delete("/{provider_id}")
async def delete_provider(
    provider_id: str,
    request: Request
):
    """Delete provider (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if provider exists
        existing_provider = await database.db.providers.find_one({"id": provider_id})
        if not existing_provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Delete provider
        await database.db.providers.delete_one({"id": provider_id})
        
        return {
            "success": True,
            "message": "Provider deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting provider: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete provider")