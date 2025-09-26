from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging
from pathlib import Path

# Import database and routes
from database import database
from routes import auth_routes, provider_routes, broker_routes, testimonial_routes

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events"""
    # Startup
    logger.info("Starting TradingHub backend...")
    await database.connect()
    
    yield
    
    # Shutdown
    logger.info("Shutting down TradingHub backend...")
    await database.disconnect()

# Create the main app
app = FastAPI(
    title="TradingHub API",
    description="API for TradingHub marketplace",
    version="1.0.0",
    lifespan=lifespan
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "TradingHub API is running", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "tradinghub-api",
        "version": "1.0.0"
    }

# Include route modules
api_router.include_router(auth_routes.router)
api_router.include_router(provider_routes.router)
api_router.include_router(broker_routes.router)
api_router.include_router(testimonial_routes.router)

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)