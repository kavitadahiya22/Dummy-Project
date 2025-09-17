"""
Penetration Testing Framework - Main FastAPI Application
=====================================================

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
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, HttpUrl, field_validator
from loguru import logger
import uvicorn
import os

from pentest_app.agents.pentest_agent import PentestAgent
from pentest_app.utils.opensearch_client import OpenSearchClient
from pentest_app.reports.vapt_final import VAPTFinalReport

# Configure logging
logger.add("logs/pentest_framework.log", rotation="10 MB", level="INFO")

# CORS configuration and app initialization will come after lifespan definition

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
    progress: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None
    start_time: datetime
    end_time: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]

# Global variables for tracking active tests
active_tests: Dict[str, Dict[str, Any]] = {}
opensearch_client = OpenSearchClient()

async def startup_event():
    """Initialize services on application startup."""
    logger.info("Starting Penetration Testing Framework")
    
    # Test OpenSearch connection
    try:
        await opensearch_client.test_connection()
        logger.info("OpenSearch connection established")
    except Exception as e:
        logger.error(f"Failed to connect to OpenSearch: {e}")

async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Penetration Testing Framework")
    await opensearch_client.close()

# Register startup and shutdown events using lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await startup_event()
    yield
    # Shutdown
    await shutdown_event()

# Update app initialization to use lifespan
app = FastAPI(
    title="Penetration Testing Framework",
    description="Ethical penetration testing framework with CrewAI agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc),
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
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modules_requested": request.modules or "all"
        })
        
        # Initialize test tracking
        active_tests[run_id] = {
            "status": "initializing",
            "target": target_url,
            "start_time": datetime.now(timezone.utc),
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
            timestamp=datetime.now(timezone.utc),
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

@app.post("/generate_report/{run_id}")
async def generate_vapt_report(run_id: str):
    """
    Generate a comprehensive VAPT report in PDF format.
    
    This endpoint fetches results from OpenSearch for the specified run_id
    and generates a professional PDF report using the Cybrty VAPT template.
    
    Args:
        run_id: Unique identifier for the penetration test
        
    Returns:
        FileResponse with the generated PDF report
        
    Raises:
        HTTPException: If run_id not found or report generation fails
    """
    try:
        logger.info(f"Generating VAPT report for run_id: {run_id}")
        
        # Check if the run exists
        if run_id not in active_tests:
            logger.warning(f"Run ID {run_id} not found in active tests")
            # Still try to fetch from OpenSearch in case it's an older run
        
        # Fetch results from OpenSearch
        opensearch_results = await opensearch_client.get_results_by_run_id(run_id)
        
        if not opensearch_results:
            logger.warning(f"No results found in OpenSearch for run_id: {run_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"No penetration test results found for run_id: {run_id}"
            )
        
        # Determine target URL
        target_url = "https://juice-shop.herokuapp.com"  # Default
        if run_id in active_tests:
            target_url = active_tests[run_id].get("target", target_url)
        elif opensearch_results and len(opensearch_results) > 0:
            # Try to extract target from first result
            first_result = opensearch_results[0]
            target_url = first_result.get("target", target_url)
        
        # Initialize VAPT report generator
        vapt_generator = VAPTFinalReport(
            run_id=run_id,
            target=target_url,
            output_dir="reports"
        )
        
        # Generate the complete report
        report_path = vapt_generator.generate_complete_report(opensearch_results)
        
        # Verify the file was created
        if not os.path.exists(report_path):
            logger.error(f"Report file not created at: {report_path}")
            raise HTTPException(
                status_code=500,
                detail="Report generation failed - file not created"
            )
        
        # Get report metadata
        report_metadata = vapt_generator.get_report_metadata()
        
        logger.info(f"VAPT report generated successfully: {report_path}")
        logger.info(f"Report metadata: {report_metadata}")
        
        # Return the PDF file as a download
        filename = vapt_generator.get_filename()
        return FileResponse(
            path=report_path,
            filename=filename,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "X-Report-Run-ID": run_id,
                "X-Report-Target": target_url,
                "X-Report-Findings": str(report_metadata.get("total_findings", 0)),
                "X-Report-Risk-Score": str(report_metadata.get("overall_risk_score", 0.0))
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Failed to generate VAPT report for run {run_id}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Report generation failed: {str(e)}"
        )

@app.get("/report_status/{run_id}")
async def get_report_status(run_id: str):
    """
    Get the status and metadata of a VAPT report.
    
    Args:
        run_id: Unique identifier for the penetration test
        
    Returns:
        Report status and metadata information
    """
    try:
        # Check if run exists
        run_exists = run_id in active_tests
        
        # Check if results exist in OpenSearch
        opensearch_results = await opensearch_client.get_results_by_run_id(run_id)
        results_exist = bool(opensearch_results)
        
        # Check if report file exists
        target_url = "https://juice-shop.herokuapp.com"
        if run_exists:
            target_url = active_tests[run_id].get("target", target_url)
        
        temp_generator = VAPTFinalReport(run_id=run_id, target=target_url)
        report_path = temp_generator.get_output_path()
        report_exists = os.path.exists(report_path)
        
        # Calculate summary statistics
        finding_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        if opensearch_results:
            for result in opensearch_results:
                severity = result.get("severity", "info").lower()
                if severity in finding_counts:
                    finding_counts[severity] += 1
        
        return {
            "run_id": run_id,
            "run_exists": run_exists,
            "results_exist": results_exist,
            "report_exists": report_exists,
            "report_filename": temp_generator.get_filename() if report_exists else None,
            "target": target_url,
            "total_findings": sum(finding_counts.values()),
            "findings_breakdown": finding_counts,
            "can_generate_report": results_exist,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get report status for run {run_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get report status: {str(e)}"
        )

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
            "end_time": datetime.now(timezone.utc),
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
            "end_time": datetime.now(timezone.utc),
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
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )