from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import List, Optional
from models import Testimonial, TestimonialCreate, TestimonialUpdate, TestimonialListResponse, TestimonialResponse
from database import database
from auth import EmergentAuth
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/testimonials", tags=["testimonials"])

# Initialize auth instance  
auth = EmergentAuth(database.db)

@router.get("/", response_model=TestimonialListResponse)
async def get_testimonials(
    approved: Optional[bool] = Query(True, description="Filter by approval status"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """Get all testimonials with optional filters"""
    try:
        # Build filter query
        filter_query = {}
        
        # Approval filter
        if approved is not None:
            filter_query["approved"] = approved
        
        # Get total count
        total = await database.db.testimonials.count_documents(filter_query)
        
        # Get testimonials with pagination
        cursor = database.db.testimonials.find(filter_query).skip(skip).limit(limit)
        testimonials_data = await cursor.to_list(length=limit)
        
        testimonials = [Testimonial(**testimonial_data) for testimonial_data in testimonials_data]
        
        return TestimonialListResponse(
            success=True,
            data=testimonials,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Error getting testimonials: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get testimonials")

@router.get("/{testimonial_id}", response_model=TestimonialResponse)
async def get_testimonial(testimonial_id: str):
    """Get single testimonial by ID"""
    try:
        testimonial_data = await database.db.testimonials.find_one({"id": testimonial_id})
        
        if not testimonial_data:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        testimonial = Testimonial(**testimonial_data)
        
        return TestimonialResponse(
            success=True,
            data=testimonial
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting testimonial: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get testimonial")

@router.post("/", response_model=TestimonialResponse)
async def create_testimonial(
    testimonial_data: TestimonialCreate,
    request: Request
):
    """Create new testimonial (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Create new testimonial
        new_testimonial = Testimonial(
            id=str(uuid.uuid4()),
            **testimonial_data.dict(),
            createdAt=datetime.now(timezone.utc)
        )
        
        # Insert into database
        await database.db.testimonials.insert_one(new_testimonial.dict())
        
        return TestimonialResponse(
            success=True,
            data=new_testimonial,
            message="Testimonial created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating testimonial: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create testimonial")

@router.put("/{testimonial_id}", response_model=TestimonialResponse)
async def update_testimonial(
    testimonial_id: str,
    testimonial_update: TestimonialUpdate,
    request: Request
):
    """Update testimonial (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if testimonial exists
        existing_testimonial = await database.db.testimonials.find_one({"id": testimonial_id})
        if not existing_testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        # Prepare update data
        update_data = testimonial_update.dict(exclude_unset=True)
        if update_data:            
            # Update testimonial
            await database.db.testimonials.update_one(
                {"id": testimonial_id},
                {"$set": update_data}
            )
        
        # Get updated testimonial
        updated_testimonial_data = await database.db.testimonials.find_one({"id": testimonial_id})
        updated_testimonial = Testimonial(**updated_testimonial_data)
        
        return TestimonialResponse(
            success=True,
            data=updated_testimonial,
            message="Testimonial updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating testimonial: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update testimonial")

@router.delete("/{testimonial_id}")
async def delete_testimonial(
    testimonial_id: str,
    request: Request
):
    """Delete testimonial (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if testimonial exists
        existing_testimonial = await database.db.testimonials.find_one({"id": testimonial_id})
        if not existing_testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        # Delete testimonial
        await database.db.testimonials.delete_one({"id": testimonial_id})
        
        return {
            "success": True,
            "message": "Testimonial deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting testimonial: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete testimonial")

@router.patch("/{testimonial_id}/approve")
async def approve_testimonial(
    testimonial_id: str,
    approved: bool,
    request: Request
):
    """Approve or reject testimonial (Admin only)"""
    try:
        # Require admin authentication
        await auth.require_admin(request)
        
        # Check if testimonial exists
        existing_testimonial = await database.db.testimonials.find_one({"id": testimonial_id})
        if not existing_testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        # Update approval status
        await database.db.testimonials.update_one(
            {"id": testimonial_id},
            {"$set": {"approved": approved}}
        )
        
        status_text = "approved" if approved else "rejected"
        
        return {
            "success": True,
            "message": f"Testimonial {status_text} successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving testimonial: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to approve testimonial")