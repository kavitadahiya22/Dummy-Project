"""
Minimal FastAPI Demo for Penetration Testing Framework
=====================================================

This is a simplified version for testing the API without all dependencies.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, field_validator

app = FastAPI(
    title="Penetration Testing Framework - Demo",
    description="Ethical penetration testing framework demo",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authorized targets
AUTHORIZED_TARGETS = [
    "https://juice-shop.herokuapp.com",
    "https://juice-shop.herokuapp.com/",
    "http://juice-shop.herokuapp.com",
    "http://juice-shop.herokuapp.com/"
]

# Mock active tests storage
active_tests: Dict[str, Dict[str, Any]] = {}

class PentestRequest(BaseModel):
    target: HttpUrl
    consent_acknowledged: bool = False
    modules: Optional[List[str]] = None
    
    @field_validator('target')
    @classmethod
    def validate_target(cls, v: HttpUrl) -> HttpUrl:
        target_str = str(v).rstrip('/')  # Remove trailing slash for comparison
        allowed_base = "juice-shop.herokuapp.com"
        
        if not (target_str.endswith(allowed_base) and 
                (target_str.startswith("http://") or target_str.startswith("https://"))):
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
    progress: Dict[str, Any]
    start_time: datetime
    end_time: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0-demo",
        timestamp=datetime.now(timezone.utc),
        services={
            "opensearch": "demo-mode",
            "crewai": "demo-mode",
            "docker": "demo-mode"
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint."""
    return await root()

@app.get("/authorized_targets")
async def get_authorized_targets():
    """Get the list of authorized targets for penetration testing."""
    return {
        "authorized_targets": AUTHORIZED_TARGETS,
        "notice": "Only these targets are authorized for penetration testing. "
                 "Testing against unauthorized targets is prohibited and may be illegal."
    }

@app.post("/invoke_pentest", response_model=PentestResponse)
async def invoke_pentest(request: PentestRequest):
    """
    Initiate a penetration test against an authorized target (DEMO MODE).
    """
    try:
        run_id = str(uuid.uuid4())
        target_url = str(request.target)
        
        print(f"DEMO: Initiating pentest for target: {target_url} (Run ID: {run_id})")
        
        # Store test info
        active_tests[run_id] = {
            "status": "demo_running",
            "target": target_url,
            "start_time": datetime.now(timezone.utc),
            "progress": {
                "current_phase": "demo_simulation",
                "completed_modules": [],
                "total_modules": 5,
                "percentage": 0
            }
        }
        
        return PentestResponse(
            run_id=run_id,
            status="initiated",
            message="DEMO: Penetration test simulation started. This is a demo version.",
            target=target_url,
            timestamp=datetime.now(timezone.utc),
            estimated_duration="Demo mode - instant results"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate penetration test: {str(e)}")

@app.get("/pentest_status/{run_id}", response_model=PentestStatus)
async def get_pentest_status(run_id: str):
    """Get the status of a running or completed penetration test."""
    if run_id not in active_tests:
        raise HTTPException(status_code=404, detail="Penetration test run not found")
    
    test_data = active_tests[run_id]
    
    # Simulate progress
    test_data["progress"]["percentage"] = min(100, test_data["progress"]["percentage"] + 20)
    if test_data["progress"]["percentage"] >= 100:
        test_data["status"] = "demo_completed"
        test_data["end_time"] = datetime.now(timezone.utc)
    
    return PentestStatus(
        run_id=run_id,
        status=test_data["status"],
        progress=test_data["progress"],
        start_time=test_data["start_time"],
        end_time=test_data.get("end_time")
    )

@app.get("/pentest_results/{run_id}")
async def get_pentest_results(run_id: str):
    """Get detailed results for a specific run (DEMO)."""
    if run_id not in active_tests:
        raise HTTPException(status_code=404, detail="Penetration test run not found")
    
    return {
        "run_id": run_id,
        "message": "This is demo mode. In production, this would show detailed security findings.",
        "demo_results": {
            "reconnaissance": "Demo: Found open ports 80, 443",
            "vulnerability_scan": "Demo: Found 3 medium severity issues",
            "exploitation": "Demo: SQL injection test completed safely",
            "summary": "Demo: This would contain real security findings in production"
        },
        "note": "Install full dependencies and configure OpenSearch for real results"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)