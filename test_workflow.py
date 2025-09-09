#!/usr/bin/env python3
"""
StateX Complete Workflow Test Script

This script simulates the complete user journey:
1. User submits contact form with text, voice, and file data
2. System sends initial confirmation notification
3. AI agents analyze and process the submission
4. System sends final analysis summary notification

Usage:
    python3 test_workflow.py                    # Interactive mode
    python3 test_workflow.py --default          # Use default test data
    python3 test_workflow.py --demo             # Run demo with sample data
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
AI_ORCHESTRATOR_URL = "http://localhost:8010"
NLP_SERVICE_URL = "http://localhost:8011"

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

class WorkflowTester:
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
    
    async def test_ai_orchestrator(self, submission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test AI orchestrator processing"""
        self.log("Testing AI orchestrator submission processing")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{AI_ORCHESTRATOR_URL}/api/process-submission",
                    json=submission_data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.log("✅ AI orchestrator submission accepted")
                        return result
                    else:
                        error_text = await response.text()
                        self.log(f"❌ AI orchestrator submission failed: {response.status} - {error_text}", "ERROR")
                        return {"success": False, "error": error_text}
        except Exception as e:
            self.log(f"❌ AI orchestrator error: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    async def test_nlp_service(self, text_content: str) -> Dict[str, Any]:
        """Test NLP service directly"""
        self.log("Testing NLP service text analysis")
        
        nlp_data = {
            "text_content": text_content,
            "requirements": "Analyze business requirements and generate comprehensive summary",
            "analysis_type": "comprehensive"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NLP_SERVICE_URL}/api/analyze-text",
                    json=nlp_data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.log("✅ NLP service analysis completed")
                        return result
                    else:
                        error_text = await response.text()
                        self.log(f"❌ NLP service failed: {response.status} - {error_text}", "ERROR")
                        return {"success": False, "error": error_text}
        except Exception as e:
            self.log(f"❌ NLP service error: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    def generate_ai_summary(self, nlp_results: Dict[str, Any], user_name: str) -> str:
        """Generate AI analysis summary for notification"""
        if not nlp_results.get("success", True):
            return f"AI analysis encountered an error: {nlp_results.get('error', 'Unknown error')}"
        
        results = nlp_results.get("results", {})
        
        summary = f"""🤖 *AI Analysis Complete for {user_name}*

📋 *Project Summary:*
{results.get('text_summary', 'Analysis completed successfully')}

🔍 *Key Insights:*
"""
        
        # Add key insights
        insights = results.get('key_insights', [])
        for i, insight in enumerate(insights[:3], 1):
            summary += f"{i}. {insight}\n"
        
        # Add business opportunities
        opportunities = results.get('business_opportunities', [])
        if opportunities:
            summary += f"\n💡 *Business Opportunities:*\n"
            for opp in opportunities[:2]:
                summary += f"• {opp.get('opportunity', 'Opportunity')} - {opp.get('potential', 'Medium')} potential\n"
        
        # Add action items
        action_items = results.get('action_items', [])
        if action_items:
            summary += f"\n📝 *Next Steps:*\n"
            for item in action_items[:3]:
                summary += f"• {item.get('action', 'Action item')} ({item.get('timeline', 'TBD')})\n"
        
        summary += f"\n⏱️ *Processing Time:* {nlp_results.get('processing_time', 0):.2f} seconds"
        summary += f"\n🎯 *Confidence:* {nlp_results.get('confidence', 0.85):.1%}"
        
        return summary
    
    async def run_complete_workflow(self, test_data: Dict[str, Any]):
        """Run the complete workflow test"""
        self.start_time = time.time()
        self.log("🚀 Starting StateX Complete Workflow Test")
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
        for i, result in enumerate(notification_results):
            if isinstance(result, Exception):
                self.log(f"❌ Notification {i+1} failed with exception: {result}", "ERROR")
            elif not result.get("success", False):
                self.log(f"❌ Notification {i+1} failed: {result.get('error', 'Unknown error')}", "ERROR")
        
        # Step 2: Prepare AI submission data
        self.log("\n🤖 Step 2: Preparing AI analysis submission")
        combined_text = f"{test_data['text_content']}\n\nVoice Transcript:\n{test_data['voice_transcript']}\n\nFile Content:\n{test_data['file_content']}"
        
        submission_data = {
            "user_id": self.session_id,
            "submission_type": "mixed",
            "text_content": combined_text,
            "voice_file_url": None,  # Simulated voice transcript
            "file_urls": [],  # Simulated file content
            "requirements": "Analyze business requirements and generate comprehensive summary",
            "contact_info": {
                "name": test_data["user_name"],
                "email": test_data["email"],
                "whatsapp": test_data["whatsapp"],
                "telegram": test_data["telegram_chat_id"]
            }
        }
        
        # Step 3: Test AI orchestrator
        self.log("🧠 Step 3: Submitting to AI orchestrator")
        orchestrator_start = time.time()
        orchestrator_result = await self.test_ai_orchestrator(submission_data)
        self.measure_time("AI Orchestrator submission", orchestrator_start)
        
        if not orchestrator_result.get("success", True):
            self.log(f"❌ AI orchestrator failed: {orchestrator_result.get('error', 'Unknown error')}", "ERROR")
            return
        
        submission_id = orchestrator_result.get("submission_id")
        self.log(f"📋 Submission ID: {submission_id}")
        
        # Step 4: Test NLP service directly (for immediate results)
        self.log("\n🔍 Step 4: Running NLP analysis")
        nlp_start = time.time()
        nlp_result = await self.test_nlp_service(combined_text)
        nlp_duration = self.measure_time("NLP Analysis", nlp_start)
        
        # Step 5: Generate and send AI summary
        self.log("\n📊 Step 5: Generating AI analysis summary")
        ai_summary = self.generate_ai_summary(nlp_result, test_data["user_name"])
        
        # Send final notification with AI results
        self.log("📱 Step 6: Sending AI analysis results")
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
        
        # Step 7: Summary and timing
        total_time = time.time() - self.start_time
        self.log("\n" + "=" * 60)
        self.log("🎉 Workflow Test Complete!")
        self.log(f"⏱️  Total Time: {total_time:.2f} seconds")
        self.log(f"🧠 NLP Analysis Time: {nlp_duration:.2f} seconds")
        self.log(f"📧 Notifications Sent: {len([r for r in final_results if not isinstance(r, Exception) and r.get('success', False)])}")
        
        # Store results
        self.results = {
            "session_id": self.session_id,
            "total_time": total_time,
            "nlp_duration": nlp_duration,
            "orchestrator_result": orchestrator_result,
            "nlp_result": nlp_result,
            "notification_results": notification_results,
            "final_results": final_results
        }
        
        return self.results

def get_user_input():
    """Get user input for test data"""
    print("\n🚀 StateX Complete Workflow Test")
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
    tester = WorkflowTester()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--default":
            print("🚀 Using default test data...")
            test_data = DEFAULT_TEST_DATA
        elif sys.argv[1] == "--demo":
            print("🚀 Running demo with sample data...")
            test_data = DEFAULT_TEST_DATA
        else:
            print("Usage: python3 test_workflow.py [--default|--demo]")
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
        print(f"   NLP Analysis: {results['nlp_duration']:.2f} seconds")
        print(f"   Status: {'✅ Success' if results['nlp_result'].get('success', True) else '❌ Failed'}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

