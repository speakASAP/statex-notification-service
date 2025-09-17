#!/usr/bin/env python3
"""
Test script for enhanced Telegram notification system
"""

import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, Any

# Test data for enhanced notification
def create_test_business_analysis() -> Dict[str, Any]:
    """Create test business analysis data"""
    return {
        "project_scope": "Develop a modern e-commerce platform with AI-powered product recommendations, real-time inventory management, and multi-channel sales integration. The platform should support B2B and B2C operations with advanced analytics and reporting capabilities.",
        "technology_stack": ["React", "Node.js", "PostgreSQL", "Redis", "Docker", "AWS", "TensorFlow"],
        "timeline_estimate": "12-16 weeks",
        "budget_range": "$50,000 - $75,000",
        "risk_factors": [
            "Complex AI integration may require additional development time",
            "Third-party API dependencies could impact timeline",
            "Scalability requirements may need infrastructure optimization"
        ],
        "market_insights": "E-commerce market is growing at 15% annually. AI-powered recommendations can increase conversion rates by 25-35%. Mobile-first approach is essential as 60% of traffic comes from mobile devices.",
        "recommendations": [
            "Implement progressive web app (PWA) for better mobile experience",
            "Use microservices architecture for better scalability",
            "Integrate with major payment gateways early in development",
            "Plan for multi-language support from the beginning"
        ],
        "confidence_score": 0.87
    }

def create_test_offer_details() -> Dict[str, Any]:
    """Create test offer details"""
    return {
        "project_id": "proj_test_12345",
        "plan_url": "http://project-proto_test_12345.localhost:3000/plan",
        "offer_url": "http://project-proto_test_12345.localhost:3000/offer",
        "pricing_tiers": [
            {
                "name": "Basic Package",
                "price": "$45,000",
                "timeline": "14 weeks",
                "features": ["Core e-commerce functionality", "Basic admin panel", "Payment integration"]
            },
            {
                "name": "Premium Package",
                "price": "$65,000",
                "timeline": "16 weeks",
                "features": ["All Basic features", "AI recommendations", "Advanced analytics", "Mobile app"]
            }
        ],
        "implementation_phases": [
            {
                "phase": "Phase 1: Foundation",
                "duration": "4 weeks",
                "deliverables": ["Project setup", "Database design", "Core API development"]
            },
            {
                "phase": "Phase 2: Core Features",
                "duration": "6 weeks",
                "deliverables": ["Product catalog", "Shopping cart", "User authentication"]
            },
            {
                "phase": "Phase 3: Advanced Features",
                "duration": "4 weeks",
                "deliverables": ["AI recommendations", "Analytics dashboard", "Admin panel"]
            },
            {
                "phase": "Phase 4: Testing & Deployment",
                "duration": "2 weeks",
                "deliverables": ["Quality assurance", "Performance optimization", "Production deployment"]
            }
        ],
        "deliverables": [
            "Fully functional e-commerce platform",
            "AI-powered recommendation engine",
            "Comprehensive admin dashboard",
            "Mobile-responsive design",
            "Payment gateway integration",
            "Analytics and reporting system",
            "Documentation and training materials"
        ],
        "next_steps": [
            "Schedule technical consultation call",
            "Review and approve project timeline",
            "Sign development agreement",
            "Begin Phase 1 development"
        ]
    }

def create_test_agent_results() -> list:
    """Create test agent results"""
    return [
        {
            "agent_id": "nlp_001",
            "agent_type": "nlp_analysis",
            "agent_name": "NLP Business Analyzer",
            "status": "completed",
            "processing_time": 12.5,
            "result_data": {
                "business_requirements": "E-commerce platform with AI features",
                "complexity_score": 8.5,
                "technical_feasibility": "High"
            },
            "confidence_score": 0.92,
            "error_message": None
        },
        {
            "agent_id": "doc_001",
            "agent_type": "document_analysis",
            "agent_name": "Document AI Processor",
            "status": "completed",
            "processing_time": 8.3,
            "result_data": {
                "documents_processed": 3,
                "key_requirements_extracted": 15,
                "technical_specifications": "Detailed"
            },
            "confidence_score": 0.88,
            "error_message": None
        },
        {
            "agent_id": "asr_001",
            "agent_type": "voice_analysis",
            "agent_name": "Voice Transcription Service",
            "status": "completed",
            "processing_time": 15.7,
            "result_data": {
                "transcript_length": 1250,
                "key_topics": ["e-commerce", "AI integration", "scalability"],
                "sentiment": "positive"
            },
            "confidence_score": 0.85,
            "error_message": None
        },
        {
            "agent_id": "proto_001",
            "agent_type": "prototype_generation",
            "agent_name": "Prototype Generator",
            "status": "failed",
            "processing_time": 5.2,
            "result_data": {},
            "confidence_score": 0.0,
            "error_message": "Template service temporarily unavailable"
        }
    ]

def create_test_file_analysis() -> list:
    """Create test file analysis summaries"""
    return [
        {
            "file_name": "business_requirements.pdf",
            "file_type": "application/pdf",
            "file_size": 2048576,  # 2MB
            "extracted_text_length": 5420,
            "key_insights": [
                "Multi-channel sales integration required",
                "B2B and B2C functionality needed",
                "Real-time inventory management essential"
            ],
            "processing_status": "completed"
        },
        {
            "file_name": "technical_specifications.docx",
            "file_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "file_size": 1536000,  # 1.5MB
            "extracted_text_length": 3200,
            "key_insights": [
                "Microservices architecture preferred",
                "Cloud-native deployment required",
                "API-first design approach"
            ],
            "processing_status": "completed"
        },
        {
            "file_name": "mockups.png",
            "file_type": "image/png",
            "file_size": 4194304,  # 4MB
            "extracted_text_length": 0,
            "key_insights": [
                "Modern UI design with clean layout",
                "Mobile-first responsive design",
                "Dark mode support included"
            ],
            "processing_status": "completed"
        }
    ]

def create_test_voice_transcription() -> Dict[str, Any]:
    """Create test voice transcription result"""
    return {
        "duration_seconds": 180.5,
        "transcript": "Hi, I'm looking to build an e-commerce platform for my business. We need something that can handle both B2B and B2C customers, with AI-powered product recommendations. The platform should integrate with our existing inventory system and support multiple payment methods. We're also interested in having a mobile app and comprehensive analytics. Our budget is flexible, but we'd like to launch within 4 months if possible.",
        "confidence_score": 0.91,
        "key_topics": [
            "e-commerce platform",
            "B2B and B2C",
            "AI recommendations",
            "inventory integration",
            "mobile app",
            "analytics"
        ],
        "processing_status": "completed"
    }

def create_test_enhanced_notification() -> Dict[str, Any]:
    """Create complete test enhanced notification request"""
    return {
        "submission_id": "sub_test_12345",
        "user_id": "user_test_001",
        "contact_info": {
            "name": "John Smith",
            "contact_type": "telegram",
            "contact_value": "694579866",  # Test Telegram chat ID
            "additional_info": {
                "email": "john.smith@example.com",
                "company": "TechStart Solutions",
                "phone": "+1-555-0123"
            }
        },
        "business_analysis": create_test_business_analysis(),
        "offer_details": create_test_offer_details(),
        "agent_results": create_test_agent_results(),
        "file_analysis_summaries": create_test_file_analysis(),
        "voice_transcription": create_test_voice_transcription(),
        "processing_summary": {
            "total_processing_time": 41.7,
            "completed_steps": 6,
            "total_steps": 7,
            "success_rate": 85.7,
            "started_at": "2024-01-15T10:30:00Z",
            "completed_at": "2024-01-15T10:30:42Z"
        },
        "notification_type": "business_offer",
        "created_at": datetime.now().isoformat()
    }

async def test_enhanced_notification():
    """Test enhanced notification functionality"""
    
    print("🧪 Testing Enhanced Telegram Notification System")
    print("=" * 60)
    
    # Create test notification data
    test_data = create_test_enhanced_notification()
    
    print(f"📋 Test Data Created:")
    print(f"   - Submission ID: {test_data['submission_id']}")
    print(f"   - Customer: {test_data['contact_info']['name']}")
    print(f"   - Contact: {test_data['contact_info']['contact_type']} ({test_data['contact_info']['contact_value']})")
    print(f"   - Agent Results: {len(test_data['agent_results'])} agents")
    print(f"   - File Analysis: {len(test_data['file_analysis_summaries'])} files")
    print(f"   - Voice Transcription: {test_data['voice_transcription']['duration_seconds']}s")
    print()
    
    # Test notification service health
    try:
        print("🔍 Checking notification service health...")
        response = requests.get("http://localhost:8005/health")
        if response.status_code == 200:
            print("✅ Notification service is healthy")
        else:
            print(f"❌ Notification service health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to notification service: {e}")
        return
    
    # Send enhanced notification
    try:
        print("📤 Sending enhanced notification...")
        response = requests.post(
            "http://localhost:8005/api/notifications/enhanced",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            notification_id = result.get("notification_id")
            print(f"✅ Enhanced notification sent successfully!")
            print(f"   - Notification ID: {notification_id}")
            print(f"   - Delivery Status: {result.get('delivery_status', {}).get('status')}")
            print(f"   - Channel: {result.get('delivery_status', {}).get('channel')}")
            
            # Wait a moment for processing
            await asyncio.sleep(2)
            
            # Check delivery status
            print("\n🔍 Checking delivery status...")
            status_response = requests.get(f"http://localhost:8005/api/notifications/enhanced/{notification_id}/status")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                delivery_status = status_data.get("delivery_status", {})
                print(f"📊 Delivery Status:")
                print(f"   - Status: {delivery_status.get('status')}")
                print(f"   - Channel: {delivery_status.get('channel')}")
                print(f"   - Attempts: {delivery_status.get('attempts')}/{delivery_status.get('max_attempts')}")
                if delivery_status.get('error_message'):
                    print(f"   - Error: {delivery_status.get('error_message')}")
                if delivery_status.get('delivery_confirmation'):
                    print(f"   - Delivered: {delivery_status.get('delivery_confirmation', {}).get('delivered_at')}")
            else:
                print(f"❌ Failed to get delivery status: {status_response.status_code}")
            
        else:
            print(f"❌ Failed to send enhanced notification: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending enhanced notification: {e}")
    
    # Test delivery statistics
    try:
        print("\n📊 Getting delivery statistics...")
        stats_response = requests.get("http://localhost:8005/api/notifications/enhanced/stats")
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            enhanced_stats = stats.get("enhanced_delivery_stats", {})
            print(f"📈 Enhanced Delivery Statistics:")
            print(f"   - Total Notifications: {enhanced_stats.get('total_notifications')}")
            print(f"   - Sent: {enhanced_stats.get('sent')}")
            print(f"   - Failed: {enhanced_stats.get('failed')}")
            print(f"   - Pending: {enhanced_stats.get('pending')}")
            print(f"   - Success Rate: {enhanced_stats.get('success_rate', 0):.1f}%")
        else:
            print(f"❌ Failed to get delivery statistics: {stats_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting delivery statistics: {e}")
    
    print("\n🎉 Enhanced notification test completed!")

def test_telegram_formatting():
    """Test Telegram message formatting without sending"""
    
    print("\n🎨 Testing Telegram Message Formatting")
    print("=" * 50)
    
    # Import formatter
    try:
        from app.telegram_formatter import TelegramBusinessOfferFormatter
        from app.models import EnhancedNotificationRequest, ContactInfo, BusinessAnalysis, OfferDetails
        
        formatter = TelegramBusinessOfferFormatter()
        
        # Create test request
        test_data = create_test_enhanced_notification()
        
        # Convert dict to Pydantic models for testing
        contact_info = ContactInfo(**test_data["contact_info"])
        business_analysis = BusinessAnalysis(**test_data["business_analysis"])
        offer_details = OfferDetails(**test_data["offer_details"])
        
        # Create enhanced request (simplified for testing)
        request = EnhancedNotificationRequest(
            submission_id=test_data["submission_id"],
            user_id=test_data["user_id"],
            contact_info=contact_info,
            business_analysis=business_analysis,
            offer_details=offer_details,
            processing_summary=test_data["processing_summary"]
        )
        
        # Format the message
        template = formatter.format_business_offer(request)
        message_parts = formatter.format_message_parts(template)
        
        print(f"📝 Formatted Message Template:")
        print(f"   - Title: {template.title}")
        print(f"   - Sections: {len(template.sections)}")
        print(f"   - Parse Mode: {template.parse_mode}")
        print(f"   - Has Keyboard: {'Yes' if template.inline_keyboard else 'No'}")
        print(f"   - Message Parts: {len(message_parts)}")
        
        # Show first message part
        if message_parts:
            print(f"\n📄 First Message Part (length: {len(message_parts[0])}):")
            print("-" * 40)
            print(message_parts[0][:500] + "..." if len(message_parts[0]) > 500 else message_parts[0])
            print("-" * 40)
        
        # Show inline keyboard
        if template.inline_keyboard:
            print(f"\n⌨️ Inline Keyboard:")
            keyboard = template.inline_keyboard.get("inline_keyboard", [])
            for row in keyboard:
                for button in row:
                    print(f"   - {button.get('text')}: {button.get('url')}")
        
        print("✅ Telegram formatting test completed!")
        
    except ImportError as e:
        print(f"❌ Cannot import formatter modules: {e}")
        print("   Make sure you're running from the notification service directory")
    except Exception as e:
        print(f"❌ Error testing formatting: {e}")

if __name__ == "__main__":
    print("🚀 StateX Enhanced Notification System Test")
    print("=" * 60)
    
    # Test formatting first (doesn't require service)
    test_telegram_formatting()
    
    # Test actual notification sending
    asyncio.run(test_enhanced_notification())