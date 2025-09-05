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
    
    # Get user input for test credentials
    print("\nPlease provide your test credentials:")
    print("(Leave empty to skip that channel)")
    
    email = input("\n📧 Email address: ").strip()
    whatsapp = input("📱 WhatsApp number (with country code, e.g., +420123456789): ").strip()
    telegram_chat_id = input("✈️ Telegram Chat ID: ").strip()
    linkedin = input("💼 LinkedIn profile URL or username: ").strip()
    
    user_name = input("\n👤 Your name (for personalization): ").strip() or "Test User"
    
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
    
    # Test LinkedIn
    if linkedin:
        print(f"\n💼 Testing LinkedIn to {linkedin}...")
        result = test_notification("linkedin", linkedin, user_name)
        if result.get("success"):
            print(f"✅ LinkedIn sent successfully! Notification ID: {result.get('notification_id')}")
        else:
            print(f"❌ LinkedIn failed: {result.get('error', result.get('message'))}")
    else:
        print("\n💼 Skipping LinkedIn test (no profile provided)")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\nTo configure real notifications, set these environment variables:")
    print("- SMTP_USERNAME and SMTP_PASSWORD for email")
    print("- TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for Telegram")
    print("- WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID for WhatsApp")
    print("- LINKEDIN_ACCESS_TOKEN for LinkedIn")

if __name__ == "__main__":
    main()
