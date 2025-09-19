"""
StateX Notification Service

Handles real notifications via email, WhatsApp, Telegram, and LinkedIn.
Enhanced with business offer formatting and delivery reliability.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import uuid
import smtplib
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel
import asyncio
import logging

# Import enhanced notification components
from .models import (
    EnhancedNotificationRequest, NotificationDeliveryStatus,
    ContactInfo, BusinessAnalysis, OfferDetails, AgentResult,
    FileAnalysisSummary, VoiceTranscriptionResult
)
from .delivery_manager import get_delivery_manager, DeliveryChannel
from .telegram_formatter import TelegramBusinessOfferFormatter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="StateX Notification Service",
    description="Handles real notifications via email, WhatsApp, Telegram, and LinkedIn",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://statex.cz", 
        "https://www.statex.cz", 
        os.getenv("CORS_ORIGIN", "http://localhost:3000"),
        "http://localhost:3002",
        f"https://localhost:{os.getenv('FRONTEND_PORT', '3000')}",
        "https://localhost:3002",
        f"http://127.0.0.1:{os.getenv('FRONTEND_PORT', '3000')}",
        "http://127.0.0.1:3002",
        f"https://127.0.0.1:{os.getenv('FRONTEND_PORT', '3000')}",
        "https://127.0.0.1:3002"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class NotificationRequest(BaseModel):
    user_id: str
    type: str  # confirmation, prototype_ready, follow_up
    title: str
    message: str
    contact_type: str  # email, whatsapp, telegram, linkedin
    contact_value: str
    user_name: Optional[str] = None

class NotificationResponse(BaseModel):
    success: bool
    message: str
    notification_id: str
    status: str
    channel: str

# Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "contact@statex.cz")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

# In-memory storage for demo purposes
notifications_db = {}

@app.on_event("startup")
async def startup_event():
    """Initialize delivery manager on startup"""
    try:
        delivery_manager = get_delivery_manager()
        await delivery_manager.start_background_processor()
        logger.info("Delivery manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize delivery manager: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup delivery manager on shutdown"""
    try:
        delivery_manager = get_delivery_manager()
        await delivery_manager.stop_background_processor()
        logger.info("Delivery manager shutdown complete")
    except Exception as e:
        logger.error(f"Error during delivery manager shutdown: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "notification-service", "timestamp": datetime.now().isoformat()}

@app.post("/api/notifications", response_model=NotificationResponse)
async def send_notification(notification: NotificationRequest):
    """Send a notification via the specified channel"""
    try:
        notification_id = str(uuid.uuid4())
        
        # Store notification record
        notification_record = {
            "id": notification_id,
            "user_id": notification.user_id,
            "type": notification.type,
            "title": notification.title,
            "message": notification.message,
            "contact_type": notification.contact_type,
            "contact_value": notification.contact_value,
            "user_name": notification.user_name,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        notifications_db[notification_id] = notification_record
        
        # Send notification based on contact type
        success = False
        status = "failed"
        channel_message = ""
        
        if notification.contact_type == "email":
            success, channel_message = await send_email_notification(notification)
        elif notification.contact_type == "whatsapp":
            success, channel_message = await send_whatsapp_notification(notification)
        elif notification.contact_type == "telegram":
            success, channel_message = await send_telegram_notification(notification)
        elif notification.contact_type == "linkedin":
            # LinkedIn profiles are collected for manual sales contact only
            success = True
            channel_message = f"LinkedIn profile {notification.contact_value} collected for manual sales contact"
        else:
            channel_message = f"Unsupported contact type: {notification.contact_type}"
        
        if success:
            status = "sent"
            notification_record["status"] = "sent"
            notification_record["sent_at"] = datetime.now().isoformat()
        else:
            status = "failed"
            notification_record["status"] = "failed"
            notification_record["error"] = channel_message
        
        notifications_db[notification_id] = notification_record
        
        return NotificationResponse(
            success=success,
            message=channel_message,
            notification_id=notification_id,
            status=status,
            channel=notification.contact_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

async def send_email_notification(notification: NotificationRequest) -> tuple[bool, str]:
    """Send email notification via SMTP"""
    try:
        # For MailHog (testing), we don't need credentials
        if SMTP_SERVER == "mailhog" or not SMTP_USERNAME or not SMTP_PASSWORD:
            # Use MailHog for testing (no credentials needed)
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            # No authentication needed for MailHog
        else:
            # Use real SMTP with credentials
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL or "contact@statex.cz"
        msg['To'] = notification.contact_value
        msg['Subject'] = notification.title
        
        # Create HTML body
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">Statex</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">AI-Powered Development Services</p>
            </div>
            <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="color: #333; margin-top: 0;">Hello {notification.user_name or 'there'}!</h2>
                <p style="color: #666; line-height: 1.6;">{notification.message}</p>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">What's Next?</h3>
                    <ul style="color: #666; line-height: 1.6;">
                        <li>We'll analyze your requirements within 24 hours</li>
                        <li>You'll receive your working prototype in 24-48 hours</li>
                        <li>We'll contact you via this email for any clarifications</li>
                    </ul>
                </div>
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    Best regards,<br>
                    The Statex Team<br>
                    <a href="https://statex.cz" style="color: #667eea;">statex.cz</a>
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL or "contact@statex.cz", notification.contact_value, text)
        server.quit()
        
        return True, f"Email sent successfully to {notification.contact_value}"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

async def send_whatsapp_notification(notification: NotificationRequest) -> tuple[bool, str]:
    """Send WhatsApp notification via WhatsApp Business API"""
    try:
        if not WHATSAPP_ACCESS_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
            return False, "WhatsApp credentials not configured"
        
        url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Format phone number (remove any non-digits, keep only digits)
        phone_number = ''.join(filter(str.isdigit, notification.contact_value))
        
        # Ensure phone number starts with country code (remove leading zeros)
        if phone_number.startswith('0'):
            phone_number = phone_number[1:]
        
        # Add country code if not present (assuming international format)
        if not phone_number.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
            # If no country code, assume it needs one - this should be handled by the user input
            pass
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": f"🚀 *Statex Notification*\n\nHello {notification.user_name or 'there'}!\n\n{notification.message}\n\nWe'll contact you via WhatsApp for updates on your prototype.\n\nBest regards,\nThe Statex Team"
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return True, f"WhatsApp message sent successfully to {notification.contact_value}"
        else:
            return False, f"WhatsApp API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Failed to send WhatsApp message: {str(e)}"

async def send_telegram_notification(notification: NotificationRequest) -> tuple[bool, str]:
    """Send Telegram notification via Telegram Bot API with inline keyboard buttons"""
    try:
        if not TELEGRAM_BOT_TOKEN:
            return False, "Telegram bot token not configured"
        
        # Use the chat ID from the notification request
        chat_id = notification.contact_value
        
        if not chat_id:
            return False, "Telegram chat ID not provided"
        
        message = f"""🚀 *Statex Notification*

Hello {notification.user_name or 'there'}!

{notification.message}

We'll contact you via Telegram for updates on your prototype.

Best regards,
The Statex Team"""
        
        # Check if this is a prototype completion notification and add buttons
        inline_keyboard = None
        if notification.type == "prototype_ready" and "prototype" in notification.message.lower():
            # Extract prototype ID from the message or use a default pattern
            prototype_id = "proto_1757889419"  # Default prototype ID
            results_url = f"http://project_{prototype_id.replace('proto_', '')}.localhost:3000/"
            dashboard_url = "http://localhost:3000/dashboard"
            new_prototype_url = "http://localhost:3000/contact"
            
            # Create inline keyboard with buttons
            inline_keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "📊 View Your Dashboard",
                            "url": dashboard_url
                        }
                    ],
                    [
                        {
                            "text": "🤖 AI Analysis Results", 
                            "url": results_url
                        }
                    ],
                    [
                        {
                            "text": "🚀 Request New Prototype",
                            "url": new_prototype_url
                        }
                    ]
                ]
            }
        
        return await send_telegram_message_with_keyboard(
            chat_id=chat_id,
            message=message,
            keyboard=inline_keyboard,
            parse_mode="Markdown"
        )
            
    except Exception as e:
        return False, f"Failed to send Telegram message: {str(e)}"

async def send_telegram_message_with_keyboard(
    chat_id: str,
    message: str,
    keyboard: Optional[Dict[str, Any]] = None,
    parse_mode: str = "Markdown"
) -> Tuple[bool, str]:
    """Send Telegram message with optional inline keyboard"""
    try:
        if not TELEGRAM_BOT_TOKEN:
            return False, "Telegram bot token not configured"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        if keyboard:
            data["reply_markup"] = keyboard
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return True, f"Telegram message sent successfully to {chat_id}"
        else:
            return False, f"Telegram API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Failed to send Telegram message: {str(e)}"


@app.get("/api/notifications")
async def get_notifications():
    """Get all notifications"""
    return {
        "success": True,
        "notifications": list(notifications_db.values()),
        "total": len(notifications_db)
    }

@app.get("/api/notifications/{notification_id}")
async def get_notification(notification_id: str):
    """Get a specific notification"""
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {
        "success": True,
        "notification": notifications_db[notification_id]
    }

@app.get("/api/notifications/stats")
async def get_notification_stats():
    """Get notification statistics"""
    total = len(notifications_db)
    sent = len([n for n in notifications_db.values() if n.get("status") == "sent"])
    failed = len([n for n in notifications_db.values() if n.get("status") == "failed"])
    
    # Get enhanced delivery stats
    delivery_manager = get_delivery_manager()
    delivery_stats = delivery_manager.get_delivery_stats()
    
    return {
        "success": True,
        "stats": {
            "total_notifications": total,
            "sent": sent,
            "failed": failed,
            "success_rate": (sent / total * 100) if total > 0 else 0
        },
        "enhanced_delivery_stats": delivery_stats
    }

@app.post("/api/notifications/enhanced", response_model=Dict[str, Any])
async def send_enhanced_notification(request: EnhancedNotificationRequest):
    """Send enhanced business offer notification with delivery reliability"""
    try:
        logger.info(f"Received enhanced notification request for submission {request.submission_id}")
        
        # Determine primary delivery channel based on contact info
        primary_channel = DeliveryChannel.TELEGRAM
        if request.contact_info.contact_type == "email":
            primary_channel = DeliveryChannel.EMAIL
        elif request.contact_info.contact_type == "whatsapp":
            primary_channel = DeliveryChannel.WHATSAPP
        
        # Send notification through delivery manager
        delivery_manager = get_delivery_manager()
        delivery_status = await delivery_manager.send_enhanced_notification(
            request=request,
            primary_channel=primary_channel
        )
        
        # Store in legacy database for compatibility
        notification_record = {
            "id": delivery_status.notification_id,
            "submission_id": request.submission_id,
            "user_id": request.user_id,
            "type": request.notification_type,
            "title": "StateX Business Analysis Complete",
            "message": "Enhanced business offer notification",
            "contact_type": request.contact_info.contact_type,
            "contact_value": request.contact_info.contact_value,
            "user_name": request.contact_info.name,
            "status": delivery_status.status,
            "created_at": request.created_at.isoformat(),
            "enhanced": True,
            "delivery_tracking": {
                "notification_id": delivery_status.notification_id,
                "channel": delivery_status.channel,
                "attempts": delivery_status.attempts,
                "max_attempts": delivery_status.max_attempts
            }
        }
        
        notifications_db[delivery_status.notification_id] = notification_record
        
        return {
            "success": True,
            "message": "Enhanced notification sent with delivery tracking",
            "notification_id": delivery_status.notification_id,
            "submission_id": request.submission_id,
            "delivery_status": {
                "status": delivery_status.status,
                "channel": delivery_status.channel,
                "attempts": delivery_status.attempts
            }
        }
        
    except Exception as e:
        logger.error(f"Error sending enhanced notification: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send enhanced notification: {str(e)}")

@app.get("/api/notifications/enhanced/{notification_id}/status")
async def get_enhanced_notification_status(notification_id: str):
    """Get delivery status of enhanced notification"""
    try:
        delivery_manager = get_delivery_manager()
        delivery_status = delivery_manager.get_delivery_status(notification_id)
        
        if not delivery_status:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {
            "success": True,
            "delivery_status": {
                "notification_id": delivery_status.notification_id,
                "submission_id": delivery_status.submission_id,
                "channel": delivery_status.channel,
                "status": delivery_status.status,
                "attempts": delivery_status.attempts,
                "max_attempts": delivery_status.max_attempts,
                "last_attempt": delivery_status.last_attempt.isoformat() if delivery_status.last_attempt else None,
                "error_message": delivery_status.error_message,
                "delivery_confirmation": delivery_status.delivery_confirmation
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting notification status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notifications/enhanced/{notification_id}/retry")
async def retry_enhanced_notification(notification_id: str):
    """Manually retry failed notification delivery"""
    try:
        delivery_manager = get_delivery_manager()
        delivery_status = delivery_manager.get_delivery_status(notification_id)
        
        if not delivery_status:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        if delivery_status.status not in ["failed", "retrying"]:
            raise HTTPException(status_code=400, detail="Notification is not in a retryable state")
        
        # Reset delivery status for retry
        delivery_status.status = "pending"
        delivery_status.attempts = 0
        delivery_status.error_message = None
        
        # This would need the original request to retry - in production, store it
        # For now, just update status
        delivery_status.status = "retrying"
        
        return {
            "success": True,
            "message": f"Notification {notification_id} queued for retry",
            "status": delivery_status.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrying notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/enhanced/stats")
async def get_enhanced_notification_stats():
    """Get enhanced notification delivery statistics"""
    try:
        delivery_manager = get_delivery_manager()
        stats = delivery_manager.get_delivery_stats()
        
        return {
            "success": True,
            "enhanced_delivery_stats": stats,
            "channels": {
                "telegram": "Primary channel for business offers",
                "email": "Fallback channel with HTML formatting",
                "whatsapp": "Fallback channel with rich text",
                "sms": "Emergency fallback (not implemented)"
            },
            "retry_policy": {
                "max_attempts": 3,
                "retry_delays": [30, 120, 300, 900],
                "fallback_enabled": True
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting enhanced stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
