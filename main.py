"""
Penetration Testing Framework - Main FastAPI Application
====================class PentestStatus(BaseModel):
    run_id: str
    status: str
    progress: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None
    start_time: datetime
    end_time: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]

# Storage for active penetration tests
active_tests: Dict[str, Dict[str, Any]] = {}=====================

This is the main entry point for the penetration testing framework.
It provides a REST API for initiating penetration tests against authorized targets.

Security Notice:
- Only authorized targets (juice-shop.herokuapp.com) are permitted
- User consent is required before any testing begins
- All activities are logged for audit purposes
"""

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl, field_validator
from loguru import logger
import uvicorn

from pentest_app.agents.pentest_agent import PentestAgent
from pentest_app.utils.opensearch_client import OpenSearchClient

# Configure logging
logger.add("logs/pentest_framework.log", rotation="10 MB", level="INFO")

app = FastAPI(
    title="Penetration Testing Framework",
    description="Ethical penetration testing framework with CrewAI agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authorized targets for penetration testing
AUTHORIZED_TARGETS = [
    "https://juice-shop.herokuapp.com",
    "http://juice-shop.herokuapp.com"
]

# Request/Response Models
class PentestRequest(BaseModel):
    target: HttpUrl
    consent_acknowledged: bool = False
    modules: Optional[List[str]] = None  # Specific modules to run
    
    @field_validator('target')
    @classmethod
    def validate_target(cls, v: HttpUrl) -> HttpUrl:
        target_str = str(v)
        if target_str not in AUTHORIZED_TARGETS:
            raise ValueError(f"Target {target_str} is not authorized. Only juice-shop.herokuapp.com is permitted.")
        return v
    
    @field_validator('consent_acknowledged')
    @classmethod
    def validate_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("User consent must be acknowledged before proceeding with penetration testing.")
        return v

class PentestResponse(BaseModel):
    run_id: str
    status: str
    message: str
    target: str
    timestamp: datetime
    estimated_duration: str

class PentestStatus(BaseModel):
    run_id: str
    status: str
    progress: Dict
    results: Optional[Dict] = None
    start_time: datetime
    end_time: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]

# Global variables for tracking active tests
active_tests: Dict[str, Dict] = {}
opensearch_client = OpenSearchClient()

@app.on_startup
async def startup_event():
    """Initialize services on application startup."""
    logger.info("Starting Penetration Testing Framework")
    
    # Test OpenSearch connection
    try:
        await opensearch_client.test_connection()
        logger.info("OpenSearch connection established")
    except Exception as e:
        logger.error(f"Failed to connect to OpenSearch: {e}")

@app.on_shutdown
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Penetration Testing Framework")
    await opensearch_client.close()

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        services={
            "opensearch": "connected" if opensearch_client.is_connected else "disconnected",
            "crewai": "ready"
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint."""
    return await root()

@app.post("/invoke_pentest", response_model=PentestResponse)
async def invoke_pentest(request: PentestRequest):
    """
    Initiate a penetration test against an authorized target.
    
    This endpoint creates a new penetration testing job using CrewAI agents.
    All activities are logged and results are stored in OpenSearch.
    
    Args:
        request: PentestRequest containing target URL and consent acknowledgment
        
    Returns:
        PentestResponse with run_id and status information
        
    Raises:
        HTTPException: If target is unauthorized or consent not provided
    """
    try:
        # Generate unique run ID
        run_id = str(uuid.uuid4())
        target_url = str(request.target)
        
        logger.info(f"Initiating pentest for target: {target_url} (Run ID: {run_id})")
        
        # Log the consent and authorization
        await opensearch_client.log_event({
            "run_id": run_id,
            "event_type": "pentest_initiated",
            "target": target_url,
            "consent_acknowledged": request.consent_acknowledged,
            "timestamp": datetime.utcnow().isoformat(),
            "modules_requested": request.modules or "all"
        })
        
        # Initialize test tracking
        active_tests[run_id] = {
            "status": "initializing",
            "target": target_url,
            "start_time": datetime.utcnow(),
            "progress": {
                "current_phase": "initialization",
                "completed_modules": [],
                "total_modules": 5,
                "percentage": 0
            }
        }
        
        # Start the penetration test asynchronously
        asyncio.create_task(run_pentest_workflow(run_id, target_url, request.modules))
        
        return PentestResponse(
            run_id=run_id,
            status="initiated",
            message="Penetration test has been started. Use the run_id to check status.",
            target=target_url,
            timestamp=datetime.utcnow(),
            estimated_duration="15-30 minutes"
        )
        
    except Exception as e:
        logger.error(f"Failed to initiate pentest: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate penetration test: {str(e)}")

@app.get("/pentest_status/{run_id}", response_model=PentestStatus)
async def get_pentest_status(run_id: str):
    """
    Get the status of a running or completed penetration test.
    
    Args:
        run_id: Unique identifier for the penetration test
        
    Returns:
        PentestStatus with current progress and results
        
    Raises:
        HTTPException: If run_id is not found
    """
    if run_id not in active_tests:
        raise HTTPException(status_code=404, detail="Penetration test run not found")
    
    test_data = active_tests[run_id]
    
    return PentestStatus(
        run_id=run_id,
        status=test_data["status"],
        progress=test_data["progress"],
        results=test_data.get("results"),
        start_time=test_data["start_time"],
        end_time=test_data.get("end_time")
    )

@app.get("/pentest_results/{run_id}")
async def get_pentest_results(run_id: str):
    """
    Get detailed results from OpenSearch for a specific run.
    
    Args:
        run_id: Unique identifier for the penetration test
        
    Returns:
        Detailed results from OpenSearch
    """
    try:
        results = await opensearch_client.get_results_by_run_id(run_id)
        return {"run_id": run_id, "results": results}
    except Exception as e:
        logger.error(f"Failed to retrieve results for run {run_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve results")

@app.get("/authorized_targets")
async def get_authorized_targets():
    """Get the list of authorized targets for penetration testing."""
    return {
        "authorized_targets": AUTHORIZED_TARGETS,
        "notice": "Only these targets are authorized for penetration testing. "
                 "Testing against unauthorized targets is prohibited and may be illegal."
    }

async def run_pentest_workflow(run_id: str, target: str, modules: Optional[List[str]] = None):
    """
    Execute the complete penetration testing workflow using CrewAI agents.
    
    Args:
        run_id: Unique identifier for this test run
        target: Target URL to test
        modules: Specific modules to run (optional)
    """
    try:
        # Update status
        active_tests[run_id]["status"] = "running"
        active_tests[run_id]["progress"]["current_phase"] = "agent_initialization"
        
        # Initialize the PentestAgent
        pentest_agent = PentestAgent(
            run_id=run_id,
            target=target,
            opensearch_client=opensearch_client
        )
        
        # Execute the penetration test
        results = await pentest_agent.execute_pentest(modules)
        
        # Update final status
        active_tests[run_id].update({
            "status": "completed",
            "end_time": datetime.utcnow(),
            "results": results,
            "progress": {
                "current_phase": "completed",
                "completed_modules": results.get("completed_modules", []),
                "total_modules": len(results.get("completed_modules", [])),
                "percentage": 100
            }
        })
        
        logger.info(f"Pentest completed successfully for run {run_id}")
        
    except Exception as e:
        logger.error(f"Pentest workflow failed for run {run_id}: {e}")
        
        # Update error status
        active_tests[run_id].update({
            "status": "failed",
            "end_time": datetime.utcnow(),
            "error": str(e),
            "progress": {
                "current_phase": "error",
                "percentage": 0
            }
        })
        
        # Log error to OpenSearch
        await opensearch_client.log_event({
            "run_id": run_id,
            "event_type": "pentest_error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )