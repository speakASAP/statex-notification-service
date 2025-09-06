#!/usr/bin/env python3
"""
Test script for StateX Notification Service

This script helps you test all notification channels with your real credentials.
"""

import requests
import json
import os
from typing import Dict, Any

# Configuration
NOTIFICATION_SERVICE_URL = "http://localhost:8005"

def test_notification(contact_type: str, contact_value: str, user_name: str = "Test User") -> Dict[str, Any]:
    """Test a notification channel"""
    
    notification_data = {
        "user_id": "test-user-123",
        "type": "confirmation",
        "title": "🚀 Statex - Form Submission Confirmed",
        "message": f"Hello {user_name}! Thank you for your form submission. We've received your request and will get back to you within 24 hours with your working prototype. We'll contact you via {contact_type} for updates.",
        "contact_type": contact_type,
        "contact_value": contact_value,
        "user_name": user_name
    }
    
    try:
        response = requests.post(
            f"{NOTIFICATION_SERVICE_URL}/api/notifications",
            json=notification_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    print("🚀 StateX Notification Service Test")
    print("=" * 50)
    
    # Default test credentials
    DEFAULT_EMAIL = "ssfskype@gmail.com"
    DEFAULT_WHATSAPP = "+420774287541"
    DEFAULT_TELEGRAM_CHAT_ID = "694579866"
    DEFAULT_USER_NAME = "Sergej"
    
    # Check if user wants to use defaults (no input)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--default":
        print("\n🚀 Using default test credentials...")
        email = DEFAULT_EMAIL
        whatsapp = DEFAULT_WHATSAPP
        telegram_chat_id = DEFAULT_TELEGRAM_CHAT_ID
        user_name = DEFAULT_USER_NAME
    else:
        print("\nPlease provide your test credentials:")
        print("(Press Enter to use default values)")
        
        email = input(f"\n📧 Email address [{DEFAULT_EMAIL}]: ").strip() or DEFAULT_EMAIL
        whatsapp = input(f"📱 WhatsApp number [{DEFAULT_WHATSAPP}]: ").strip() or DEFAULT_WHATSAPP
        telegram_chat_id = input(f"✈️ Telegram Chat ID [{DEFAULT_TELEGRAM_CHAT_ID}]: ").strip() or DEFAULT_TELEGRAM_CHAT_ID
        
        user_name = input(f"\n👤 Your name [{DEFAULT_USER_NAME}]: ").strip() or DEFAULT_USER_NAME
    
    print(f"\n🧪 Testing notifications for {user_name}...")
    print("=" * 50)
    
    # Test Email
    if email:
        print(f"\n📧 Testing Email to {email}...")
        result = test_notification("email", email, user_name)
        if result.get("success"):
            print(f"✅ Email sent successfully! Notification ID: {result.get('notification_id')}")
        else:
            print(f"❌ Email failed: {result.get('error', result.get('message'))}")
    else:
        print("\n📧 Skipping email test (no email provided)")
    
    # Test WhatsApp
    if whatsapp:
        print(f"\n📱 Testing WhatsApp to {whatsapp}...")
        result = test_notification("whatsapp", whatsapp, user_name)
        if result.get("success"):
            print(f"✅ WhatsApp sent successfully! Notification ID: {result.get('notification_id')}")
        else:
            print(f"❌ WhatsApp failed: {result.get('error', result.get('message'))}")
    else:
        print("\n📱 Skipping WhatsApp test (no number provided)")
    
    # Test Telegram
    if telegram_chat_id:
        print(f"\n✈️ Testing Telegram to {telegram_chat_id}...")
        result = test_notification("telegram", telegram_chat_id, user_name)
        if result.get("success"):
            print(f"✅ Telegram sent successfully! Notification ID: {result.get('notification_id')}")
        else:
            print(f"❌ Telegram failed: {result.get('error', result.get('message'))}")
    else:
        print("\n✈️ Skipping Telegram test (no chat ID provided)")
    
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\nTo configure real notifications, set these environment variables:")
    print("- SMTP_USERNAME and SMTP_PASSWORD for email")
    print("- TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for Telegram")
    print("- WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID for WhatsApp")

if __name__ == "__main__":
    main()
