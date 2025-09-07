#!/usr/bin/env python3
"""
StateX Simplified Workflow Test Script

This script demonstrates the complete user journey with the current architecture:
1. User submits contact form with text, voice, and file data
2. System sends initial confirmation notification
3. Simulates AI analysis (since AI services aren't running)
4. System sends final analysis summary notification

Usage:
    python3 test_workflow_simple.py                    # Interactive mode
    python3 test_workflow_simple.py --default          # Use default test data
    python3 test_workflow_simple.py --demo             # Run demo with sample data
"""

import requests
import json
import time
import uuid
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List
import asyncio
import aiohttp

# Configuration
NOTIFICATION_SERVICE_URL = "http://localhost:8005"

# Default test data
DEFAULT_TEST_DATA = {
    "user_name": "Sergej",
    "email": "ssfskype@gmail.com",
    "whatsapp": "+420774287541",
    "telegram_chat_id": "694579866",
    "text_content": "I want to create a website for my auto car repairing business. The website should have online booking, customer management, service history tracking, and payment processing. I also need a mobile app for my technicians to manage their schedules and update job statuses.",
    "voice_transcript": "Hi, I'm Sergej and I run an auto repair shop. I need a digital solution to modernize my business. My customers are always calling to book appointments and it's hard to keep track of everything. I want something that can handle online bookings, send reminders, track service history, and maybe even process payments. The system should work on both computer and mobile devices.",
    "file_content": "Business Requirements Document:\n\n1. Online Booking System\n   - Customer can book appointments 24/7\n   - Real-time availability calendar\n   - Email/SMS confirmations\n\n2. Customer Management\n   - Customer profiles with service history\n   - Vehicle information tracking\n   - Communication preferences\n\n3. Service Management\n   - Job tracking and status updates\n   - Parts inventory management\n   - Technician scheduling\n\n4. Payment Processing\n   - Online payment acceptance\n   - Invoice generation\n   - Payment history tracking\n\n5. Mobile Application\n   - Technician dashboard\n   - Real-time job updates\n   - Customer communication"
}

class SimplifiedWorkflowTester:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = None
        self.results = {}
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def measure_time(self, operation: str, start_time: float):
        """Measure and log operation time"""
        duration = time.time() - start_time
        self.log(f"{operation} completed in {duration:.2f} seconds")
        return duration
        
    async def test_notification_service(self, contact_type: str, contact_value: str, user_name: str, message: str) -> Dict[str, Any]:
        """Test notification service"""
        self.log(f"Testing {contact_type} notification to {contact_value}")
        
        notification_data = {
            "user_id": self.session_id,
            "type": "confirmation",
            "title": "StateX Submission Received",
            "message": message,
            "contact_type": contact_type,
            "contact_value": contact_value,
            "user_name": user_name
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NOTIFICATION_SERVICE_URL}/api/notifications",
                    json=notification_data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.log(f"✅ {contact_type.title()} notification sent successfully")
                        return result
                    else:
                        error_text = await response.text()
                        self.log(f"❌ {contact_type.title()} notification failed: {response.status} - {error_text}", "ERROR")
                        return {"success": False, "error": error_text}
        except Exception as e:
            self.log(f"❌ {contact_type.title()} notification error: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    def simulate_ai_analysis(self, text_content: str, user_name: str) -> Dict[str, Any]:
        """Simulate AI analysis (since AI services aren't running)"""
        self.log("🤖 Simulating AI analysis...")
        
        # Simulate processing time
        time.sleep(2)
        
        # Generate realistic analysis results
        analysis_results = {
            "text_summary": f"User {user_name} wants to create a comprehensive digital solution for their auto repair business, including online booking, customer management, service tracking, and payment processing.",
            "key_insights": [
                "Business needs digital transformation for auto repair shop",
                "Requires multi-platform solution (web + mobile)",
                "Focus on customer experience and operational efficiency",
                "Integration of booking, management, and payment systems"
            ],
            "business_opportunities": [
                {
                    "opportunity": "Web-based booking system",
                    "description": "24/7 online appointment scheduling with real-time availability",
                    "potential": "High"
                },
                {
                    "opportunity": "Mobile technician app",
                    "description": "Field management app for technicians to manage schedules and job updates",
                    "potential": "High"
                },
                {
                    "opportunity": "Customer portal",
                    "description": "Self-service portal for customers to view service history and manage bookings",
                    "potential": "Medium"
                }
            ],
            "action_items": [
                {
                    "action": "Conduct market research for auto repair software",
                    "priority": "High",
                    "timeline": "1-2 weeks"
                },
                {
                    "action": "Develop MVP prototype with core booking functionality",
                    "priority": "High",
                    "timeline": "4-6 weeks"
                },
                {
                    "action": "Create technical architecture for multi-platform solution",
                    "priority": "Medium",
                    "timeline": "2-3 weeks"
                }
            ],
            "technical_requirements": {
                "frontend": ["React/Next.js", "React Native", "Responsive design", "Real-time updates"],
                "backend": ["Node.js/Python", "RESTful API", "WebSocket support", "Database design"],
                "integrations": ["Payment processing", "SMS/Email notifications", "Calendar sync", "Inventory management"]
            },
            "confidence": 0.87,
            "processing_time": 2.1
        }
        
        self.log("✅ AI analysis simulation completed")
        return analysis_results
    
    def generate_ai_summary(self, analysis_results: Dict[str, Any], user_name: str) -> str:
        """Generate AI analysis summary for notification"""
        summary = f"""🤖 *AI Analysis Complete for {user_name}*

📋 *Project Summary:*
{analysis_results['text_summary']}

🔍 *Key Insights:*
"""
        
        # Add key insights
        for i, insight in enumerate(analysis_results['key_insights'], 1):
            summary += f"{i}. {insight}\n"
        
        # Add business opportunities
        summary += f"\n💡 *Business Opportunities:*\n"
        for opp in analysis_results['business_opportunities']:
            summary += f"• {opp['opportunity']} - {opp['potential']} potential\n"
        
        # Add action items
        summary += f"\n📝 *Next Steps:*\n"
        for item in analysis_results['action_items']:
            summary += f"• {item['action']} ({item['timeline']})\n"
        
        summary += f"\n⏱️ *Processing Time:* {analysis_results['processing_time']:.1f} seconds"
        summary += f"\n🎯 *Confidence:* {analysis_results['confidence']:.1%}"
        
        return summary
    
    async def run_complete_workflow(self, test_data: Dict[str, Any]):
        """Run the complete workflow test"""
        self.start_time = time.time()
        self.log("🚀 Starting StateX Simplified Workflow Test")
        self.log("=" * 60)
        
        # Step 1: Send initial confirmation notifications
        self.log("📧 Step 1: Sending initial confirmation notifications")
        confirmation_message = f"""Hello {test_data['user_name']}!

Thank you for your submission! We've received your project details:
• Text description: {len(test_data['text_content'])} characters
• Voice transcript: {len(test_data['voice_transcript'])} characters  
• File content: {len(test_data['file_content'])} characters

Our AI agents are now analyzing your requirements. We'll contact you via Telegram with the analysis results shortly.

Best regards,
The Statex Team"""
        
        # Test all notification channels
        notification_tasks = []
        for contact_type, contact_value in [
            ("email", test_data["email"]),
            ("whatsapp", test_data["whatsapp"]),
            ("telegram", test_data["telegram_chat_id"])
        ]:
            task = self.test_notification_service(
                contact_type, contact_value, test_data["user_name"], confirmation_message
            )
            notification_tasks.append(task)
        
        notification_results = await asyncio.gather(*notification_tasks, return_exceptions=True)
        
        # Log notification results
        successful_notifications = 0
        for i, result in enumerate(notification_results):
            if isinstance(result, Exception):
                self.log(f"❌ Notification {i+1} failed with exception: {result}", "ERROR")
            elif result.get("success", False):
                successful_notifications += 1
            else:
                self.log(f"❌ Notification {i+1} failed: {result.get('error', 'Unknown error')}", "ERROR")
        
        self.log(f"📊 Notifications sent: {successful_notifications}/3")
        
        # Step 2: Simulate AI analysis
        self.log("\n🤖 Step 2: Simulating AI analysis")
        combined_text = f"{test_data['text_content']}\n\nVoice Transcript:\n{test_data['voice_transcript']}\n\nFile Content:\n{test_data['file_content']}"
        
        ai_start = time.time()
        ai_results = self.simulate_ai_analysis(combined_text, test_data["user_name"])
        ai_duration = self.measure_time("AI Analysis Simulation", ai_start)
        
        # Step 3: Generate and send AI summary
        self.log("\n📊 Step 3: Generating AI analysis summary")
        ai_summary = self.generate_ai_summary(ai_results, test_data["user_name"])
        
        # Send final notification with AI results
        self.log("📱 Step 4: Sending AI analysis results")
        final_notification_tasks = []
        for contact_type, contact_value in [
            ("email", test_data["email"]),
            ("whatsapp", test_data["whatsapp"]),
            ("telegram", test_data["telegram_chat_id"])
        ]:
            task = self.test_notification_service(
                contact_type, contact_value, test_data["user_name"], ai_summary
            )
            final_notification_tasks.append(task)
        
        final_results = await asyncio.gather(*final_notification_tasks, return_exceptions=True)
        
        # Count successful final notifications
        successful_final = 0
        for result in final_results:
            if not isinstance(result, Exception) and result.get("success", False):
                successful_final += 1
        
        # Step 4: Summary and timing
        total_time = time.time() - self.start_time
        self.log("\n" + "=" * 60)
        self.log("🎉 Workflow Test Complete!")
        self.log(f"⏱️  Total Time: {total_time:.2f} seconds")
        self.log(f"🧠 AI Analysis Time: {ai_duration:.2f} seconds")
        self.log(f"📧 Initial Notifications: {successful_notifications}/3")
        self.log(f"📱 Final Notifications: {successful_final}/3")
        
        # Store results
        self.results = {
            "session_id": self.session_id,
            "total_time": total_time,
            "ai_duration": ai_duration,
            "ai_results": ai_results,
            "notification_results": notification_results,
            "final_results": final_results,
            "successful_notifications": successful_notifications,
            "successful_final": successful_final
        }
        
        return self.results

def get_user_input():
    """Get user input for test data"""
    print("\n🚀 StateX Simplified Workflow Test")
    print("=" * 50)
    print("This test simulates the complete user journey from contact form to AI analysis.")
    print("\nPlease provide your test credentials:")
    print("(Press Enter to use default values)")
    
    user_name = input(f"\n👤 Your name [{DEFAULT_TEST_DATA['user_name']}]: ").strip() or DEFAULT_TEST_DATA['user_name']
    email = input(f"📧 Email address [{DEFAULT_TEST_DATA['email']}]: ").strip() or DEFAULT_TEST_DATA['email']
    whatsapp = input(f"📱 WhatsApp number [{DEFAULT_TEST_DATA['whatsapp']}]: ").strip() or DEFAULT_TEST_DATA['whatsapp']
    telegram_chat_id = input(f"✈️ Telegram Chat ID [{DEFAULT_TEST_DATA['telegram_chat_id']}]: ").strip() or DEFAULT_TEST_DATA['telegram_chat_id']
    
    print(f"\n📝 Project description:")
    print(f"Current: {DEFAULT_TEST_DATA['text_content'][:100]}...")
    use_default_text = input("Use default project description? (y/n) [y]: ").strip().lower() or "y"
    
    if use_default_text == "y":
        text_content = DEFAULT_TEST_DATA['text_content']
        voice_transcript = DEFAULT_TEST_DATA['voice_transcript']
        file_content = DEFAULT_TEST_DATA['file_content']
    else:
        text_content = input("Enter your project description: ").strip()
        voice_transcript = input("Enter voice transcript (or press Enter to skip): ").strip()
        file_content = input("Enter file content (or press Enter to skip): ").strip()
    
    return {
        "user_name": user_name,
        "email": email,
        "whatsapp": whatsapp,
        "telegram_chat_id": telegram_chat_id,
        "text_content": text_content,
        "voice_transcript": voice_transcript,
        "file_content": file_content
    }

async def main():
    """Main function"""
    tester = SimplifiedWorkflowTester()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--default":
            print("🚀 Using default test data...")
            test_data = DEFAULT_TEST_DATA
        elif sys.argv[1] == "--demo":
            print("🚀 Running demo with sample data...")
            test_data = DEFAULT_TEST_DATA
        else:
            print("Usage: python3 test_workflow_simple.py [--default|--demo]")
            sys.exit(1)
    else:
        test_data = get_user_input()
    
    # Run the complete workflow
    try:
        results = await tester.run_complete_workflow(test_data)
        
        # Print final summary
        print(f"\n📊 Test Results Summary:")
        print(f"   Session ID: {results['session_id']}")
        print(f"   Total Time: {results['total_time']:.2f} seconds")
        print(f"   AI Analysis: {results['ai_duration']:.2f} seconds")
        print(f"   Initial Notifications: {results['successful_notifications']}/3")
        print(f"   Final Notifications: {results['successful_final']}/3")
        print(f"   Status: {'✅ Success' if results['successful_final'] > 0 else '❌ Failed'}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

