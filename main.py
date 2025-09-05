import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Beehiiv Integration Backend", version="1.0.0")

# Pydantic models
class SubscribeRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    source: Optional[str] = "website"

class SubscribeResponse(BaseModel):
    success: bool
    message: str
    subscriber_id: Optional[str] = None

class BeehiivAPI:
    def __init__(self):
        self.api_key = os.getenv("BEEHIIV_API_KEY")
        self.publication_id = os.getenv("BEEHIIV_PUBLICATION_ID")
        self.base_url = "https://api.beehiiv.com/v2"
        
        if not self.api_key:
            raise ValueError("BEEHIIV_API_KEY environment variable is required")
        if not self.publication_id:
            raise ValueError("BEEHIIV_PUBLICATION_ID environment variable is required")
    
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def subscribe_user(self, email: str, first_name: str = None, last_name: str = None, source: str = "website"):
        """Subscribe a user to the Beehiiv publication"""
        try:
            url = f"{self.base_url}/publications/{self.publication_id}/subscriptions"
            
            payload = {
                "email": email,
                "reactivate_existing": True,
                "send_welcome_email": True,
                "utm_source": source
            }
            
            # Add name fields if provided
            if first_name:
                payload["first_name"] = first_name
            if last_name:
                payload["last_name"] = last_name
            
            response = requests.post(url, json=payload, headers=self.get_headers())
            
            if response.status_code == 201:
                data = response.json()
                logger.info(f"Successfully subscribed {email} to Beehiiv")
                return {
                    "success": True,
                    "subscriber_id": data.get("id"),
                    "message": "Successfully subscribed to newsletter"
                }
            elif response.status_code == 409:
                # User already exists
                logger.info(f"User {email} already subscribed")
                return {
                    "success": True,
                    "message": "Email already subscribed to newsletter"
                }
            else:
                logger.error(f"Beehiiv API error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "message": f"Failed to subscribe: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }

# Initialize Beehiiv API
try:
    beehiiv_api = BeehiivAPI()
except ValueError as e:
    logger.error(f"Configuration error: {str(e)}")
    beehiiv_api = None

@app.get("/")
async def root():
    return {"message": "Beehiiv Integration Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "beehiiv-integration"}

@app.post("/subscribe", response_model=SubscribeResponse)
async def subscribe_user(request: SubscribeRequest):
    """
    Subscribe a user to the Beehiiv newsletter
    """
    if not beehiiv_api:
        raise HTTPException(
            status_code=500, 
            detail="Beehiiv API not properly configured"
        )
    
    try:
        result = beehiiv_api.subscribe_user(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            source=request.source
        )
        
        if result["success"]:
            return SubscribeResponse(
                success=True,
                message=result["message"],
                subscriber_id=result.get("subscriber_id")
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Subscription error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during subscription"
        )

@app.get("/publication-info")
async def get_publication_info():
    """
    Get information about the Beehiiv publication
    """
    if not beehiiv_api:
        raise HTTPException(
            status_code=500, 
            detail="Beehiiv API not properly configured"
        )
    
    try:
        url = f"{beehiiv_api.base_url}/publications/{beehiiv_api.publication_id}"
        response = requests.get(url, headers=beehiiv_api.get_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch publication info: {response.text}"
            )
    except Exception as e:
        logger.error(f"Publication info error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# Cloud Functions entry point
def app_handler(request):
    """Entry point for Google Cloud Functions"""
    from functions_framework import create_app
    return create_app(app)
