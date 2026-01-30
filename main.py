"""
Quiz Automation API
FastAPI server for processing QR URLs with multiple users
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import logging
from pathlib import Path
from automate import run_for_user

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Quiz Automation API",
    description="API for automating quiz login and QR processing for multiple users",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
def root():
    """Root endpoint - Health check"""
    return {
        "status": "running",
        "service": "Quiz Automation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "process_qr": "/process-qr (POST)"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "quiz-automation"}


# Request/Response models
class ProcessQRRequest(BaseModel):
    qr_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "qr_url": "https://jeeto16cr.com/q/R6RcHQ"
            }
        }


class UserResult(BaseModel):
    mobile: str
    status: str
    error: str = None


class ProcessQRResponse(BaseModel):
    qr_url: str
    results: list[UserResult]
    total_users: int
    successful: int
    failed: int


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Quiz Automation API is running",
        "endpoints": {
            "POST /process-qr": "Process QR URL for all users",
            "GET /users": "Get list of users",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    users_file = Path("users.json")
    return {
        "status": "healthy",
        "users_file_exists": users_file.exists()
    }


@app.get("/users")
def get_users():
    """Get list of all users (without passwords)"""
    try:
        users_file = Path("users.json")
        if not users_file.exists():
            raise HTTPException(status_code=404, detail="users.json not found")
        
        with open(users_file) as f:
            users = json.load(f)
        
        # Return users without passwords
        safe_users = [{"mobile": user.get("mobile")} for user in users]
        
        return {
            "total_users": len(safe_users),
            "users": safe_users
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in users.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process-qr")
def process_qr(payload: ProcessQRRequest):
    """
    Process QR URL for all users
    
    Args:
        payload: ProcessQRRequest with qr_url
        
    Returns:
        ProcessQRResponse with results for all users
    """
    qr_url = payload.qr_url
    
    logger.info(f"Received request to process QR URL: {qr_url}")

    if not qr_url:
        raise HTTPException(status_code=400, detail="qr_url is required")

    # Load users
    try:
        users_file = Path("users.json")
        if not users_file.exists():
            raise HTTPException(status_code=404, detail="users.json not found")
        
        with open(users_file) as f:
            users = json.load(f)
        
        if not users or len(users) == 0:
            raise HTTPException(status_code=400, detail="No users found in users.json")
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in users.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading users: {str(e)}")

    logger.info(f"Processing for {len(users)} users...")
    
    results = []

    # Process each user
    for idx, user in enumerate(users, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing user {idx}/{len(users)}")
        logger.info(f"{'='*60}")
        
        result = run_for_user(user, qr_url)
        results.append(result)
        
        logger.info(f"User {idx} result: {result['status']}")

    # Calculate statistics
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "error")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"SUMMARY: Total={len(users)}, Success={successful}, Failed={failed}")
    logger.info(f"{'='*60}\n")

    return {
        "qr_url": qr_url,
        "results": results,
        "total_users": len(users),
        "successful": successful,
        "failed": failed
    }


# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
