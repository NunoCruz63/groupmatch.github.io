from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import List, Optional
from models import Broker, BrokerCreate, BrokerUpdate, BrokerListResponse, BrokerResponse
from database import database
from auth import EmergentAuth
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/brokers", tags=["brokers"])

# Initialize auth instance  
auth = EmergentAuth(database.db)

@router.get("/", response_model=BrokerListResponse)
async def get_brokers(
    instrumentType: Optional[str] = Query(None, description="Filter by instrument type"),
    minDeposit: Optional[str] = Query(None, description="Filter by minimum deposit"), 
    regulation: Optional[str] = Query(None, description="Filter by regulation"),
    search: Optional[str] = Query(None, description="Search in name and instruments"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """Get all brokers with optional filters"""
    try:
        # Build filter query
        filter_query = {}
        
        # Instrument type filter
        if instrumentType and instrumentType != "all":
            filter_query["instruments"] = instrumentType
        
        # Min deposit filter
        if minDeposit and minDeposit != "all":
            max_deposit = int(minDeposit)
            filter_query["minDeposit"] = {"$lte": max_deposit}
        
        # Regulation filter
        if regulation and regulation != "all":
            filter_query["regulation"] = regulation
        
        # Search filter
        if search:
            search_regex = {"$regex": search, "$options": "i"}
            filter_query["$or"] = [
                {"name": search_regex},
                {"instruments": {"$elemMatch": search_regex}}
            ]
        
        # Get total count
        total = await database.db.brokers.count_documents(filter_query)
        
        # Get brokers with pagination
        cursor = database.db.brokers.find(filter_query).skip(skip).limit(limit)
        brokers_data = await cursor.to_list(length=limit)
        
        brokers = [Broker(**broker_data) for broker_data in brokers_data]
        
        return BrokerListResponse(
            success=True,
            data=brokers,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Error getting brokers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get brokers")

@router.get("/search")
async def search_brokers(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=50)
):
    """Search brokers by name or instruments"""
    try:
        search_regex = {"$regex": q, "$options": "i"}
        filter_query = {
            "$or": [
                {"name": search_regex},
                {"instruments": {"$elemMatch": search_regex}}
            ]
        }
        
        cursor = database.db.brokers.find(filter_query).limit(limit)
        brokers_data = await cursor.to_list(length=limit)
        
        brokers = [Broker(**broker_data) for broker_data in brokers_data]
        
        return BrokerListResponse(
            success=True,
            data=brokers,
            total=len(brokers)
        )
        
    except Exception as e:
        logger.error(f"Error searching brokers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search brokers")

@router.get("/{broker_id}", response_model=BrokerResponse)
async def get_broker(broker_id: str):
    """Get single broker by ID"""
    try:
        broker_data = await database.db.brokers.find_one({"id": broker_id})
        
        if not broker_data:
            raise HTTPException(status_code=404, detail="Broker not found")
        
        broker = Broker(**broker_data)
        
        return BrokerResponse(
            success=True,
            data=broker
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting broker: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get broker")

@router.post("/", response_model=BrokerResponse)
async def create_broker(
    broker_data: BrokerCreate,
    request: Request
):
    """Create new broker (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Create new broker
        new_broker = Broker(
            id=str(uuid.uuid4()),
            **broker_data.dict(),
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        
        # Insert into database
        await database.db.brokers.insert_one(new_broker.dict())
        
        return BrokerResponse(
            success=True,
            data=new_broker,
            message="Broker created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating broker: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create broker")

@router.put("/{broker_id}", response_model=BrokerResponse)
async def update_broker(
    broker_id: str,
    broker_update: BrokerUpdate,
    request: Request
):
    """Update broker (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if broker exists
        existing_broker = await database.db.brokers.find_one({"id": broker_id})
        if not existing_broker:
            raise HTTPException(status_code=404, detail="Broker not found")
        
        # Prepare update data
        update_data = broker_update.dict(exclude_unset=True)
        if update_data:
            update_data["updatedAt"] = datetime.now(timezone.utc)
            
            # Update broker
            await database.db.brokers.update_one(
                {"id": broker_id},
                {"$set": update_data}
            )
        
        # Get updated broker
        updated_broker_data = await database.db.brokers.find_one({"id": broker_id})
        updated_broker = Broker(**updated_broker_data)
        
        return BrokerResponse(
            success=True,
            data=updated_broker,
            message="Broker updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating broker: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update broker")

@router.delete("/{broker_id}")
async def delete_broker(
    broker_id: str,
    request: Request
):
    """Delete broker (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if broker exists
        existing_broker = await database.db.brokers.find_one({"id": broker_id})
        if not existing_broker:
            raise HTTPException(status_code=404, detail="Broker not found")
        
        # Delete broker
        await database.db.brokers.delete_one({"id": broker_id})
        
        return {
            "success": True,
            "message": "Broker deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting broker: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete broker")