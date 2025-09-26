from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone

# Provider Model
class ProviderBase(BaseModel):
    name: str
    winRate: int = Field(..., ge=0, le=100)
    tradesLastMonth: int = Field(..., ge=0)
    signalTypes: List[str]
    subscriptionPrice: int = Field(..., ge=0)
    currency: str = "USD"
    rating: float = Field(..., ge=0, le=5)
    followers: int = Field(..., ge=0)
    description: str
    riskLevel: str
    avgPipsProfitMonthly: int = Field(..., ge=0)
    verified: bool = True
    affiliateUrl: str

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    winRate: Optional[int] = Field(None, ge=0, le=100)
    tradesLastMonth: Optional[int] = Field(None, ge=0)
    signalTypes: Optional[List[str]] = None
    subscriptionPrice: Optional[int] = Field(None, ge=0)
    currency: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    followers: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    riskLevel: Optional[str] = None
    avgPipsProfitMonthly: Optional[int] = Field(None, ge=0)
    verified: Optional[bool] = None
    affiliateUrl: Optional[str] = None

class Provider(ProviderBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Broker Model
class BrokerBase(BaseModel):
    name: str
    accountTypes: List[str]
    minDeposit: int = Field(..., ge=0)
    maxLeverage: str
    spreadsFrom: float = Field(..., ge=0)
    currency: str = "USD"
    bonus: Optional[str] = None
    rating: float = Field(..., ge=0, le=5)
    regulation: List[str]
    instruments: List[str]
    platformsSupported: List[str]
    withdrawalTime: str
    customerSupport: str
    verified: bool = True
    affiliateUrl: str

class BrokerCreate(BrokerBase):
    pass

class BrokerUpdate(BaseModel):
    name: Optional[str] = None
    accountTypes: Optional[List[str]] = None
    minDeposit: Optional[int] = Field(None, ge=0)
    maxLeverage: Optional[str] = None
    spreadsFrom: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None
    bonus: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    regulation: Optional[List[str]] = None
    instruments: Optional[List[str]] = None
    platformsSupported: Optional[List[str]] = None
    withdrawalTime: Optional[str] = None
    customerSupport: Optional[str] = None
    verified: Optional[bool] = None
    affiliateUrl: Optional[str] = None

class Broker(BrokerBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Testimonial Model
class TestimonialBase(BaseModel):
    name: str
    role: str
    avatar: str
    rating: int = Field(..., ge=1, le=5)
    text: str
    location: str
    approved: bool = True

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    avatar: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None
    location: Optional[str] = None
    approved: Optional[bool] = None

class Testimonial(TestimonialBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# User Model (for Emergent Auth)
class User(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    session_token: Optional[str] = None
    session_expires: Optional[datetime] = None
    is_admin: bool = False
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lastLogin: Optional[datetime] = None

class SessionData(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    session_token: str

# Response Models
class ProviderResponse(BaseModel):
    success: bool
    data: Optional[Provider] = None
    message: Optional[str] = None

class ProviderListResponse(BaseModel):
    success: bool
    data: List[Provider] = []
    total: int = 0
    message: Optional[str] = None

class BrokerResponse(BaseModel):
    success: bool
    data: Optional[Broker] = None
    message: Optional[str] = None

class BrokerListResponse(BaseModel):
    success: bool
    data: List[Broker] = []
    total: int = 0
    message: Optional[str] = None

class TestimonialResponse(BaseModel):
    success: bool
    data: Optional[Testimonial] = None
    message: Optional[str] = None

class TestimonialListResponse(BaseModel):
    success: bool
    data: List[Testimonial] = []
    total: int = 0
    message: Optional[str] = None