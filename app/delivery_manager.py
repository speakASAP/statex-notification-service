"""
Notification delivery reliability manager with retry logic and fallback channels
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import uuid
import json

from .models import (
    NotificationDeliveryStatus, EnhancedNotificationRequest,
    ContactInfo, NotificationTemplate
)
from .telegram_formatter import TelegramBusinessOfferFormatter

logger = logging.getLogger(__name__)

class DeliveryChannel(str, Enum):
    TELEGRAM = "telegram"
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    SMS = "sms"

class DeliveryStatus(str, Enum):
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"

class NotificationDeliveryManager:
    """Manages notification delivery with retry logic and fallback channels"""
    
    def __init__(self):
        self.delivery_queue: Dict[str, NotificationDeliveryStatus] = {}
        self.retry_delays = [30, 120, 300, 900]  # 30s, 2m, 5m, 15m
        self.max_retries = 3
        self.fallback_channels = {
            DeliveryChannel.TELEGRAM: [DeliveryChannel.EMAIL, DeliveryChannel.WHATSAPP],
            DeliveryChannel.EMAIL: [DeliveryChannel.TELEGRAM, DeliveryChannel.WHATSAPP],
            DeliveryChannel.WHATSAPP: [DeliveryChannel.EMAIL, DeliveryChannel.TELEGRAM],
        }
        self.formatter = TelegramBusinessOfferFormatter()
        self._retry_task = None
        
    async def start_background_processor(self):
        """Start the background retry processor"""
        if self._retry_task is None:
            self._retry_task = asyncio.create_task(self._process_retry_queue())
    
    async def stop_background_processor(self):
        """Stop the background retry processor"""
        if self._retry_task:
            self._retry_task.cancel()
            try:
                await self._retry_task
            except asyncio.CancelledError:
                pass
            self._retry_task = None
    
    async def send_enhanced_notification(
        self,
        request: EnhancedNotificationRequest,
        primary_channel: DeliveryChannel = DeliveryChannel.TELEGRAM
    ) -> NotificationDeliveryStatus:
        """Send enhanced notification with delivery tracking"""
        
        notification_id = str(uuid.uuid4())
        
        # Create delivery status record
        delivery_status = NotificationDeliveryStatus(
            notification_id=notification_id,
            submission_id=request.submission_id,
            channel=primary_channel.value,
            status=DeliveryStatus.PENDING.value,
            attempts=0,
            max_attempts=self.max_retries
        )
        
        self.delivery_queue[notification_id] = delivery_status
        
        # Start delivery process
        await self._attempt_delivery(notification_id, request, primary_channel)
        
        return delivery_status
    
    async def _attempt_delivery(
        self,
        notification_id: str,
        request: EnhancedNotificationRequest,
        channel: DeliveryChannel
    ) -> bool:
        """Attempt to deliver notification via specified channel"""
        
        delivery_status = self.delivery_queue[notification_id]
        delivery_status.status = DeliveryStatus.SENDING.value
        delivery_status.attempts += 1
        delivery_status.last_attempt = datetime.now()
        
        try:
            success = False
            error_message = None
            
            if channel == DeliveryChannel.TELEGRAM:
                success, error_message = await self._send_telegram_notification(request)
            elif channel == DeliveryChannel.EMAIL:
                success, error_message = await self._send_email_notification(request)
            elif channel == DeliveryChannel.WHATSAPP:
                success, error_message = await self._send_whatsapp_notification(request)
            elif channel == DeliveryChannel.SMS:
                success, error_message = await self._send_sms_notification(request)
            
            if success:
                delivery_status.status = DeliveryStatus.SENT.value
                delivery_status.delivery_confirmation = {
                    "delivered_at": datetime.now().isoformat(),
                    "channel": channel.value,
                    "message": "Notification delivered successfully"
                }
                logger.info(f"Notification {notification_id} delivered successfully via {channel.value}")
                return True
            else:
                delivery_status.error_message = error_message
                await self._handle_delivery_failure(notification_id, request, channel)
                return False
                
        except Exception as e:
            delivery_status.error_message = str(e)
            logger.error(f"Delivery attempt failed for {notification_id}: {e}")
            await self._handle_delivery_failure(notification_id, request, channel)
            return False
    
    async def _handle_delivery_failure(
        self,
        notification_id: str,
        request: EnhancedNotificationRequest,
        failed_channel: DeliveryChannel
    ):
        """Handle delivery failure with retry logic and fallback channels"""
        
        delivery_status = self.delivery_queue[notification_id]
        
        # Check if we should retry on the same channel
        if delivery_status.attempts < delivery_status.max_attempts:
            delivery_status.status = DeliveryStatus.RETRYING.value
            
            # Schedule retry with exponential backoff
            retry_delay = self.retry_delays[min(delivery_status.attempts - 1, len(self.retry_delays) - 1)]
            logger.info(f"Scheduling retry for {notification_id} in {retry_delay} seconds")
            
            asyncio.create_task(self._schedule_retry(notification_id, request, failed_channel, retry_delay))
        else:
            # Try fallback channels
            await self._try_fallback_channels(notification_id, request, failed_channel)
    
    async def _schedule_retry(
        self,
        notification_id: str,
        request: EnhancedNotificationRequest,
        channel: DeliveryChannel,
        delay: int
    ):
        """Schedule a retry attempt after specified delay"""
        
        await asyncio.sleep(delay)
        
        # Check if notification is still in retry status
        if notification_id in self.delivery_queue:
            delivery_status = self.delivery_queue[notification_id]
            if delivery_status.status == DeliveryStatus.RETRYING.value:
                await self._attempt_delivery(notification_id, request, channel)
    
    async def _try_fallback_channels(
        self,
        notification_id: str,
        request: EnhancedNotificationRequest,
        failed_channel: DeliveryChannel
    ):
        """Try fallback channels when primary channel fails"""
        
        delivery_status = self.delivery_queue[notification_id]
        fallback_channels = self.fallback_channels.get(failed_channel, [])
        
        for fallback_channel in fallback_channels:
            # Check if we have contact info for this channel
            if self._has_contact_info_for_channel(request.contact_info, fallback_channel):
                logger.info(f"Trying fallback channel {fallback_channel.value} for {notification_id}")
                
                # Reset attempts for fallback channel
                delivery_status.attempts = 0
                delivery_status.channel = fallback_channel.value
                
                success = await self._attempt_delivery(notification_id, request, fallback_channel)
                if success:
                    return
        
        # All channels failed
        delivery_status.status = DeliveryStatus.FAILED.value
        logger.error(f"All delivery channels failed for notification {notification_id}")
    
    def _has_contact_info_for_channel(self, contact_info: ContactInfo, channel: DeliveryChannel) -> bool:
        """Check if contact info is available for specified channel"""
        
        if channel == DeliveryChannel.TELEGRAM:
            return contact_info.contact_type == "telegram" or "telegram_id" in contact_info.additional_info
        elif channel == DeliveryChannel.EMAIL:
            return contact_info.contact_type == "email" or "email" in contact_info.additional_info
        elif channel == DeliveryChannel.WHATSAPP:
            return contact_info.contact_type == "whatsapp" or "whatsapp" in contact_info.additional_info
        elif channel == DeliveryChannel.SMS:
            return contact_info.contact_type == "phone" or "phone" in contact_info.additional_info
        
        return False
    
    async def _send_telegram_notification(self, request: EnhancedNotificationRequest) -> Tuple[bool, Optional[str]]:
        """Send notification via Telegram with enhanced formatting"""
        
        try:
            # Format the business offer
            template = self.formatter.format_business_offer(request)
            message_parts = self.formatter.format_message_parts(template)
            
            # Get Telegram chat ID
            chat_id = request.contact_info.contact_value
            if request.contact_info.contact_type != "telegram":
                chat_id = request.contact_info.additional_info.get("telegram_id")
            
            if not chat_id:
                return False, "No Telegram chat ID available"
            
            # Import here to avoid circular imports
            from .main import send_telegram_message_with_keyboard
            
            # Send message parts
            for i, message_part in enumerate(message_parts):
                # Only add keyboard to the last message
                keyboard = template.inline_keyboard if i == len(message_parts) - 1 else None
                
                success, error = await send_telegram_message_with_keyboard(
                    chat_id=chat_id,
                    message=message_part,
                    keyboard=keyboard,
                    parse_mode=template.parse_mode
                )
                
                if not success:
                    return False, error
                
                # Small delay between messages to avoid rate limiting
                if i < len(message_parts) - 1:
                    await asyncio.sleep(0.5)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    async def _send_email_notification(self, request: EnhancedNotificationRequest) -> Tuple[bool, Optional[str]]:
        """Send notification via email with business offer formatting"""
        
        try:
            # Format business offer for email
            email_content = self._format_business_offer_for_email(request)
            
            # Get email address
            email = request.contact_info.contact_value
            if request.contact_info.contact_type != "email":
                email = request.contact_info.additional_info.get("email")
            
            if not email:
                return False, "No email address available"
            
            # Import here to avoid circular imports
            from .main import send_email_notification
            from .main import NotificationRequest
            
            # Create email notification request
            email_request = NotificationRequest(
                user_id=request.user_id,
                type="business_offer",
                title="StateX Business Analysis Complete - Your Custom Offer",
                message=email_content,
                contact_type="email",
                contact_value=email,
                user_name=request.contact_info.name
            )
            
            return await send_email_notification(email_request)
            
        except Exception as e:
            return False, str(e)
    
    async def _send_whatsapp_notification(self, request: EnhancedNotificationRequest) -> Tuple[bool, Optional[str]]:
        """Send notification via WhatsApp with business offer formatting"""
        
        try:
            # Format business offer for WhatsApp
            whatsapp_content = self._format_business_offer_for_whatsapp(request)
            
            # Get WhatsApp number
            whatsapp = request.contact_info.contact_value
            if request.contact_info.contact_type != "whatsapp":
                whatsapp = request.contact_info.additional_info.get("whatsapp")
            
            if not whatsapp:
                return False, "No WhatsApp number available"
            
            # Import here to avoid circular imports
            from .main import send_whatsapp_notification
            from .main import NotificationRequest
            
            # Create WhatsApp notification request
            whatsapp_request = NotificationRequest(
                user_id=request.user_id,
                type="business_offer",
                title="StateX Business Analysis Complete",
                message=whatsapp_content,
                contact_type="whatsapp",
                contact_value=whatsapp,
                user_name=request.contact_info.name
            )
            
            return await send_whatsapp_notification(whatsapp_request)
            
        except Exception as e:
            return False, str(e)
    
    async def _send_sms_notification(self, request: EnhancedNotificationRequest) -> Tuple[bool, Optional[str]]:
        """Send notification via SMS (placeholder implementation)"""
        
        # SMS implementation would go here
        # For now, return not implemented
        return False, "SMS delivery not implemented"
    
    def _format_business_offer_for_email(self, request: EnhancedNotificationRequest) -> str:
        """Format business offer for email delivery"""
        
        content = f"""
Dear {request.contact_info.name},

Your StateX business analysis is complete! Our AI agents have processed your submission and generated a comprehensive business offer.

SUBMISSION DETAILS:
- Submission ID: {request.submission_id}
- Processed: {request.created_at.strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if request.business_analysis:
            content += f"""
BUSINESS ANALYSIS SUMMARY:
- Project Scope: {request.business_analysis.project_scope[:200]}...
- Technology Stack: {', '.join(request.business_analysis.technology_stack)}
- Timeline: {request.business_analysis.timeline_estimate}
- Budget Range: {request.business_analysis.budget_range}
"""
        
        if request.offer_details:
            content += f"""
PROJECT LINKS:
- View Project Plan: {request.offer_details.plan_url}
- View Detailed Offer: {request.offer_details.offer_url}
"""
        
        content += f"""
PROCESSING SUMMARY:
- Total Processing Time: {request.processing_summary.get('total_processing_time', 0):.1f} seconds
- Successful Steps: {request.processing_summary.get('completed_steps', 0)}/{request.processing_summary.get('total_steps', 0)}

Next Steps:
1. Review your detailed project plan and offer
2. Contact our sales team for any questions
3. Schedule a consultation call to discuss implementation

Best regards,
The StateX Team
https://statex.cz
contact@statex.cz
"""
        
        return content
    
    def _format_business_offer_for_whatsapp(self, request: EnhancedNotificationRequest) -> str:
        """Format business offer for WhatsApp delivery"""
        
        content = f"""🚀 *StateX Business Analysis Complete*

Hello {request.contact_info.name}!

Your AI-powered business analysis is ready! 

📋 *Submission:* {request.submission_id}
📅 *Processed:* {request.created_at.strftime('%Y-%m-%d %H:%M')}

"""
        
        if request.business_analysis:
            content += f"""🧠 *Analysis Summary:*
• Timeline: {request.business_analysis.timeline_estimate}
• Budget: {request.business_analysis.budget_range}
• Tech Stack: {', '.join(request.business_analysis.technology_stack[:3])}

"""
        
        if request.offer_details:
            content += f"""🔗 *Your Project Links:*
📋 Plan: {request.offer_details.plan_url}
💰 Offer: {request.offer_details.offer_url}

"""
        
        content += f"""⏱️ *Processing:* {request.processing_summary.get('total_processing_time', 0):.1f}s
✅ *Success Rate:* {request.processing_summary.get('completed_steps', 0)}/{request.processing_summary.get('total_steps', 0)} steps

Ready to bring your project to life? Contact us!

Best regards,
The StateX Team 🏢"""
        
        return content
    
    async def _process_retry_queue(self):
        """Background task to process retry queue"""
        
        while True:
            try:
                # Process any pending retries
                current_time = datetime.now()
                
                for notification_id, delivery_status in list(self.delivery_queue.items()):
                    if delivery_status.status == DeliveryStatus.RETRYING.value:
                        # Check if retry time has passed
                        if delivery_status.last_attempt:
                            time_since_attempt = current_time - delivery_status.last_attempt
                            retry_delay = self.retry_delays[min(delivery_status.attempts - 1, len(self.retry_delays) - 1)]
                            
                            if time_since_attempt.total_seconds() >= retry_delay:
                                logger.info(f"Processing retry for notification {notification_id}")
                                # This would need the original request - in production, store it
                                # For now, just mark as failed
                                delivery_status.status = DeliveryStatus.FAILED.value
                
                # Clean up old completed/failed notifications (older than 24 hours)
                cutoff_time = current_time - timedelta(hours=24)
                for notification_id, delivery_status in list(self.delivery_queue.items()):
                    if (delivery_status.status in [DeliveryStatus.SENT.value, DeliveryStatus.FAILED.value] and
                        delivery_status.last_attempt and
                        delivery_status.last_attempt < cutoff_time):
                        del self.delivery_queue[notification_id]
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in retry queue processor: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    def get_delivery_status(self, notification_id: str) -> Optional[NotificationDeliveryStatus]:
        """Get delivery status for a notification"""
        return self.delivery_queue.get(notification_id)
    
    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics"""
        
        total = len(self.delivery_queue)
        sent = len([d for d in self.delivery_queue.values() if d.status == DeliveryStatus.SENT.value])
        failed = len([d for d in self.delivery_queue.values() if d.status == DeliveryStatus.FAILED.value])
        pending = len([d for d in self.delivery_queue.values() if d.status in [DeliveryStatus.PENDING.value, DeliveryStatus.SENDING.value, DeliveryStatus.RETRYING.value]])
        
        return {
            "total_notifications": total,
            "sent": sent,
            "failed": failed,
            "pending": pending,
            "success_rate": (sent / total * 100) if total > 0 else 0,
            "failure_rate": (failed / total * 100) if total > 0 else 0
        }

# Global delivery manager instance (will be initialized in main.py)
delivery_manager = None

def get_delivery_manager() -> NotificationDeliveryManager:
    """Get or create the global delivery manager instance"""
    global delivery_manager
    if delivery_manager is None:
        delivery_manager = NotificationDeliveryManager()
    return delivery_manager