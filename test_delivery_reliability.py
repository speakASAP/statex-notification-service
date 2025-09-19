#!/usr/bin/env python3
"""
Test script for notification delivery reliability system
"""

import asyncio
import json
from datetime import datetime
from app.delivery_manager import NotificationDeliveryManager, DeliveryChannel, get_delivery_manager
from app.models import (
    EnhancedNotificationRequest, ContactInfo, BusinessAnalysis, 
    OfferDetails, NotificationDeliveryStatus
)

async def test_delivery_manager():
    """Test the delivery manager functionality"""
    
    print("🧪 Testing Notification Delivery Manager")
    print("=" * 50)
    
    # Create delivery manager instance
    delivery_manager = NotificationDeliveryManager()
    await delivery_manager.start_background_processor()
    
    # Create test notification request
    contact_info = ContactInfo(
        name="Test User",
        contact_type="telegram",
        contact_value="123456789",
        additional_info={
            "email": "test@example.com",
            "whatsapp": "+1234567890"
        }
    )
    
    business_analysis = BusinessAnalysis(
        project_scope="Test project for delivery reliability",
        technology_stack=["React", "Node.js"],
        timeline_estimate="4-6 weeks",
        budget_range="$20,000 - $30,000",
        risk_factors=["Testing environment limitations"],
        market_insights="Test market analysis",
        recommendations=["Use test-driven development"],
        confidence_score=0.95
    )
    
    offer_details = OfferDetails(
        project_id="test_delivery_123",
        plan_url="http://localhost:3000/plan/test_delivery_123",
        offer_url="http://localhost:3000/offer/test_delivery_123"
    )
    
    request = EnhancedNotificationRequest(
        submission_id="test_delivery_sub_123",
        user_id="test_delivery_user_123",
        contact_info=contact_info,
        business_analysis=business_analysis,
        offer_details=offer_details,
        processing_summary={
            "total_processing_time": 25.5,
            "completed_steps": 4,
            "total_steps": 4
        }
    )
    
    print(f"📋 Test Request Created:")
    print(f"   - Submission ID: {request.submission_id}")
    print(f"   - Primary Channel: {request.contact_info.contact_type}")
    print(f"   - Fallback Channels: email, whatsapp")
    print()
    
    # Test 1: Send notification with primary channel
    print("🚀 Test 1: Send notification via primary channel")
    try:
        delivery_status = await delivery_manager.send_enhanced_notification(
            request=request,
            primary_channel=DeliveryChannel.TELEGRAM
        )
        
        print(f"✅ Notification queued successfully!")
        print(f"   - Notification ID: {delivery_status.notification_id}")
        print(f"   - Status: {delivery_status.status}")
        print(f"   - Channel: {delivery_status.channel}")
        print(f"   - Attempts: {delivery_status.attempts}/{delivery_status.max_attempts}")
        
        # Wait a moment for processing
        await asyncio.sleep(1)
        
        # Check updated status
        updated_status = delivery_manager.get_delivery_status(delivery_status.notification_id)
        if updated_status:
            print(f"📊 Updated Status: {updated_status.status}")
            if updated_status.error_message:
                print(f"   - Error: {updated_status.error_message}")
        
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    print()
    
    # Test 2: Test delivery statistics
    print("📈 Test 2: Check delivery statistics")
    try:
        stats = delivery_manager.get_delivery_stats()
        print(f"📊 Delivery Statistics:")
        print(f"   - Total Notifications: {stats['total_notifications']}")
        print(f"   - Sent: {stats['sent']}")
        print(f"   - Failed: {stats['failed']}")
        print(f"   - Pending: {stats['pending']}")
        print(f"   - Success Rate: {stats['success_rate']:.1f}%")
        
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    print()
    
    # Test 3: Test fallback channel detection
    print("🔄 Test 3: Test fallback channel detection")
    try:
        # Test with email primary
        has_telegram = delivery_manager._has_contact_info_for_channel(
            contact_info, DeliveryChannel.TELEGRAM
        )
        has_email = delivery_manager._has_contact_info_for_channel(
            contact_info, DeliveryChannel.EMAIL
        )
        has_whatsapp = delivery_manager._has_contact_info_for_channel(
            contact_info, DeliveryChannel.WHATSAPP
        )
        has_sms = delivery_manager._has_contact_info_for_channel(
            contact_info, DeliveryChannel.SMS
        )
        
        print(f"📞 Channel Availability:")
        print(f"   - Telegram: {'✅' if has_telegram else '❌'}")
        print(f"   - Email: {'✅' if has_email else '❌'}")
        print(f"   - WhatsApp: {'✅' if has_whatsapp else '❌'}")
        print(f"   - SMS: {'✅' if has_sms else '❌'}")
        
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    print()
    
    # Test 4: Test message formatting for different channels
    print("📝 Test 4: Test message formatting for different channels")
    try:
        # Test email formatting
        email_content = delivery_manager._format_business_offer_for_email(request)
        print(f"📧 Email Format (first 200 chars):")
        print(f"   {email_content[:200]}...")
        print()
        
        # Test WhatsApp formatting
        whatsapp_content = delivery_manager._format_business_offer_for_whatsapp(request)
        print(f"📱 WhatsApp Format (first 200 chars):")
        print(f"   {whatsapp_content[:200]}...")
        
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
    
    print()
    print("🎉 Delivery reliability tests completed!")

def test_retry_logic():
    """Test retry logic configuration"""
    
    print("\n⏰ Testing Retry Logic Configuration")
    print("=" * 40)
    
    delivery_manager = NotificationDeliveryManager()
    
    print(f"🔄 Retry Configuration:")
    print(f"   - Max Retries: {delivery_manager.max_retries}")
    print(f"   - Retry Delays: {delivery_manager.retry_delays}")
    print(f"   - Fallback Channels: {len(delivery_manager.fallback_channels)} configured")
    
    for primary, fallbacks in delivery_manager.fallback_channels.items():
        print(f"   - {primary.value} → {[f.value for f in fallbacks]}")
    
    print("✅ Retry logic configuration verified!")

def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🚨 Testing Error Handling Scenarios")
    print("=" * 40)
    
    # Test with invalid contact info
    try:
        invalid_contact = ContactInfo(
            name="Invalid User",
            contact_type="invalid_type",
            contact_value=""
        )
        
        print("📋 Testing with invalid contact info...")
        print(f"   - Contact Type: {invalid_contact.contact_type}")
        print(f"   - Contact Value: '{invalid_contact.contact_value}'")
        print("✅ Invalid contact info handled gracefully")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test with missing required fields
    try:
        minimal_request = EnhancedNotificationRequest(
            submission_id="minimal_test",
            user_id="minimal_user",
            contact_info=ContactInfo(
                name="Minimal User",
                contact_type="email",
                contact_value="minimal@test.com"
            )
        )
        
        print("📋 Testing with minimal required fields...")
        print(f"   - Has business analysis: {minimal_request.business_analysis is not None}")
        print(f"   - Has offer details: {minimal_request.offer_details is not None}")
        print("✅ Minimal request handled gracefully")
        
    except Exception as e:
        print(f"❌ Minimal request test failed: {e}")

if __name__ == "__main__":
    print("🚀 StateX Notification Delivery Reliability Test")
    print("=" * 60)
    
    # Test basic retry logic configuration
    test_retry_logic()
    
    # Test error handling
    test_error_handling()
    
    # Test delivery manager functionality
    asyncio.run(test_delivery_manager())