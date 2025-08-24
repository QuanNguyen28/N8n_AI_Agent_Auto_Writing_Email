# src/app/routers/send_email_router.py
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import logging
import os
import json
from datetime import datetime

router = APIRouter()

class SendEmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    metadata: Optional[Dict[str, Any]] = None

class SendEmailResponse(BaseModel):
    status: str
    message: Optional[str] = None
    logged_at: Optional[str] = None

log_dir = os.getenv("LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("send_email")
if not logger.handlers:
    handler = logging.FileHandler(os.path.join(log_dir, "send_email.log"))
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

@router.post("/", response_model=SendEmailResponse)
async def send_email(payload: SendEmailRequest = Body(...)):
    """
    Mock send-email endpoint.
    Behavior:
      - validate payload via pydantic
      - log payload to file and stdout
      - return success status (does NOT send real email)
    To implement real sending later, replace the logging block with SMTP / provider call.
    """
    try:
        log_entry = {
            "to": payload.to,
            "subject": payload.subject,
            "body_preview": payload.body[:500],  
            "metadata": payload.metadata or {},
            "received_at": datetime.utcnow().isoformat() + "Z"
        }

        # Log to file (structured JSON line) and also info log
        logger.info(json.dumps(log_entry, ensure_ascii=False))
        logging.getLogger("uvicorn").info(f"Mock send-email logged: to={payload.to}, subject={payload.subject}")

        return SendEmailResponse(status="ok", message="Email logged (mock)", logged_at=log_entry["received_at"])
    except Exception as e:
        logging.getLogger("uvicorn").error(f"Error in send_email mock: {e}")
        raise HTTPException(status_code=500, detail="Internal error logging email")