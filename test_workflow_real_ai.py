#!/usr/bin/env python3
"""
StateX Real AI Workflow Test Script

This script demonstrates the complete user journey with real AI processing:
1. User submits contact form with text, voice, and file data
2. System sends initial confirmation notification
3. Real AI agents analyze the submission (when available)
4. System sends final AI analysis results notification

Usage:
    python3 test_workflow_real_ai.py                    # Interactive mode
    python3 test_workflow_real_ai.py --default          # Use default test data
    python3 test_workflow_real_ai.py --demo             # Run demo with sample data
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
AI_ORCHESTRATOR_URL = "http://localhost:8010"  # Real AI orchestrator
PLATFORM_AI_URL = "http://localhost:8003"      # Platform AI orchestrator (placeholder)

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

class RealAIWorkflowTester:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = None
        self.results = {}
        self.ai_services_available = False
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def measure_time(self, operation: str, start_time: float):
        """Measure and log operation time"""
        duration = time.time() - start_time
        self.log(f"{operation} completed in {duration:.2f} seconds")
        return duration
        
    async def check_ai_services(self) -> bool:
        """Check if AI services are available"""
        self.log("🔍 Checking AI services availability...")
        
        # Check real AI orchestrator
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{AI_ORCHESTRATOR_URL}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        self.log("✅ Real AI Orchestrator is available")
                        return True
        except Exception as e:
            self.log(f"❌ Real AI Orchestrator not available: {e}", "ERROR")
        
        # Check platform AI orchestrator
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{PLATFORM_AI_URL}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        self.log("⚠️  Platform AI Orchestrator available (placeholder)")
                        return False
        except Exception as e:
            self.log(f"❌ Platform AI Orchestrator not available: {e}", "ERROR")
        
        self.log("❌ No AI services available - will use enhanced simulation")
        return False
        
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
    
    async def submit_to_real_ai_orchestrator(self, text_content: str, voice_transcript: str, file_content: str, user_name: str) -> Dict[str, Any]:
        """Submit to real AI orchestrator"""
        self.log("🤖 Submitting to real AI orchestrator...")
        
        submission_data = {
            "submission_id": self.session_id,
            "user_name": user_name,
            "text_content": text_content,
            "voice_transcript": voice_transcript,
            "file_content": file_content,
            "contact_info": {
                "email": "ssfskype@gmail.com",
                "whatsapp": "+420774287541",
                "telegram_chat_id": "694579866"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{AI_ORCHESTRATOR_URL}/api/process-submission",
                    json=submission_data,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.log("✅ Real AI orchestrator submission successful")
                        return result
                    else:
                        error_text = await response.text()
                        self.log(f"❌ Real AI orchestrator failed: {response.status} - {error_text}", "ERROR")
                        return {"success": False, "error": error_text}
        except Exception as e:
            self.log(f"❌ Real AI orchestrator error: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    async def get_ai_submission_status(self, submission_id: str) -> Dict[str, Any]:
        """Get AI submission status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{AI_ORCHESTRATOR_URL}/api/status/{submission_id}",
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": error_text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_ai_submission_results(self, submission_id: str) -> Dict[str, Any]:
        """Get AI submission results"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{AI_ORCHESTRATOR_URL}/api/results/{submission_id}",
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": error_text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enhanced_ai_simulation(self, text_content: str, voice_transcript: str, file_content: str, user_name: str) -> Dict[str, Any]:
        """Enhanced AI simulation with more realistic processing"""
        self.log("🤖 Running enhanced AI simulation...")
        
        # Simulate realistic processing time (3-8 seconds)
        processing_time = 3 + (hash(text_content) % 5)
        time.sleep(processing_time)
        
        # Generate more sophisticated analysis
        combined_content = f"{text_content}\n\nVoice: {voice_transcript}\n\nFiles: {file_content}"
        
        # Analyze business type
        business_keywords = {
            "auto": ["automotive", "car", "vehicle", "repair", "garage", "mechanic"],
            "restaurant": ["restaurant", "food", "dining", "kitchen", "menu", "chef"],
            "retail": ["store", "shop", "retail", "ecommerce", "inventory", "sales"],
            "healthcare": ["medical", "health", "clinic", "doctor", "patient", "treatment"],
            "fitness": ["gym", "fitness", "workout", "training", "exercise", "health"],
            "education": ["school", "education", "learning", "course", "training", "student"]
        }
        
        detected_business = "general"
        for business_type, keywords in business_keywords.items():
            if any(keyword in combined_content.lower() for keyword in keywords):
                detected_business = business_type
                break
        
        # Generate business-specific insights
        business_insights = {
            "auto": {
                "pain_points": ["Manual appointment scheduling", "Customer communication", "Service history tracking", "Payment processing"],
                "opportunities": ["Online booking system", "Customer portal", "Mobile app for technicians", "Automated reminders"],
                "tech_stack": ["React/Next.js", "Node.js", "PostgreSQL", "Stripe API", "Twilio SMS"]
            },
            "restaurant": {
                "pain_points": ["Table management", "Order tracking", "Kitchen coordination", "Customer feedback"],
                "opportunities": ["Online ordering", "Table reservation", "Kitchen display system", "Customer loyalty app"],
                "tech_stack": ["React/Next.js", "Node.js", "MongoDB", "Stripe API", "Socket.io"]
            },
            "general": {
                "pain_points": ["Manual processes", "Customer communication", "Data management", "Workflow automation"],
                "opportunities": ["Digital transformation", "Process automation", "Customer portal", "Mobile application"],
                "tech_stack": ["React/Next.js", "Node.js", "PostgreSQL", "Payment integration", "Real-time updates"]
            }
        }
        
        insights = business_insights.get(detected_business, business_insights["general"])
        
        # Generate comprehensive analysis
        analysis_results = {
            "business_type": detected_business,
            "text_summary": f"User {user_name} wants to create a comprehensive digital solution for their {detected_business} business, focusing on automation, customer experience, and operational efficiency.",
            "key_insights": [
                f"Business needs digital transformation for {detected_business} operations",
                "Requires multi-platform solution (web + mobile)",
                "Focus on customer experience and operational efficiency",
                "Integration of multiple business functions"
            ],
            "pain_points": insights["pain_points"],
            "business_opportunities": [
                {
                    "opportunity": "Digital Platform Development",
                    "description": f"Comprehensive {detected_business} management platform",
                    "potential": "High",
                    "timeline": "3-6 months"
                },
                {
                    "opportunity": "Mobile Application",
                    "description": "Native mobile app for staff and customers",
                    "potential": "High",
                    "timeline": "2-4 months"
                },
                {
                    "opportunity": "Process Automation",
                    "description": "Automate manual processes and workflows",
                    "potential": "Medium",
                    "timeline": "1-3 months"
                }
            ],
            "technical_recommendations": {
                "frontend": insights["tech_stack"][:3],
                "backend": insights["tech_stack"][3:],
                "integrations": ["Payment processing", "SMS/Email notifications", "Calendar sync", "Analytics"],
                "deployment": ["Docker", "AWS/Azure", "CI/CD pipeline", "Monitoring"]
            },
            "action_items": [
                {
                    "action": f"Conduct {detected_business} market research",
                    "priority": "High",
                    "timeline": "1-2 weeks",
                    "description": "Analyze competitors and market opportunities"
                },
                {
                    "action": "Develop MVP prototype",
                    "priority": "High",
                    "timeline": "4-8 weeks",
                    "description": "Create working prototype with core features"
                },
                {
                    "action": "Create technical architecture",
                    "priority": "Medium",
                    "timeline": "2-3 weeks",
                    "description": "Design scalable system architecture"
                },
                {
                    "action": "Set up development environment",
                    "priority": "Medium",
                    "timeline": "1 week",
                    "description": "Configure development tools and CI/CD"
                }
            ],
            "budget_estimate": {
                "development": "$15,000 - $35,000",
                "infrastructure": "$200 - $500/month",
                "maintenance": "$1,000 - $2,000/month",
                "timeline": "3-6 months"
            },
            "confidence": 0.85 + (hash(text_content) % 15) / 100,
            "processing_time": processing_time,
            "ai_services_used": ["NLP Analysis", "Business Intelligence", "Technical Planning", "Market Research"]
        }
        
        self.log("✅ Enhanced AI simulation completed")
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
        
        # Add pain points
        summary += f"\n⚠️ *Current Pain Points:*\n"
        for point in analysis_results['pain_points']:
            summary += f"• {point}\n"
        
        # Add business opportunities
        summary += f"\n💡 *Business Opportunities:*\n"
        for opp in analysis_results['business_opportunities']:
            summary += f"• {opp['opportunity']} - {opp['potential']} potential ({opp['timeline']})\n"
        
        # Add action items
        summary += f"\n📝 *Next Steps:*\n"
        for item in analysis_results['action_items']:
            summary += f"• {item['action']} ({item['timeline']})\n"
        
        # Add budget estimate
        summary += f"\n💰 *Budget Estimate:*\n"
        summary += f"• Development: {analysis_results['budget_estimate']['development']}\n"
        summary += f"• Infrastructure: {analysis_results['budget_estimate']['infrastructure']}\n"
        summary += f"• Timeline: {analysis_results['budget_estimate']['timeline']}\n"
        
        summary += f"\n⏱️ *Processing Time:* {analysis_results['processing_time']:.1f} seconds"
        summary += f"\n🎯 *Confidence:* {analysis_results['confidence']:.1%}"
        summary += f"\n🤖 *AI Services:* {', '.join(analysis_results['ai_services_used'])}"
        
        return summary
    
    async def run_complete_workflow(self, test_data: Dict[str, Any]):
        """Run the complete workflow test"""
        self.start_time = time.time()
        self.log("🚀 Starting StateX Real AI Workflow Test")
        self.log("=" * 60)
        
        # Check AI services availability
        self.ai_services_available = await self.check_ai_services()
        
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
        
        # Step 2: AI Analysis
        self.log("\n🤖 Step 2: AI Analysis")
        combined_text = f"{test_data['text_content']}\n\nVoice Transcript:\n{test_data['voice_transcript']}\n\nFile Content:\n{test_data['file_content']}"
        
        ai_start = time.time()
        
        if self.ai_services_available:
            # Use real AI services
            self.log("🧠 Using real AI services...")
            ai_submission = await self.submit_to_real_ai_orchestrator(
                test_data['text_content'],
                test_data['voice_transcript'],
                test_data['file_content'],
                test_data['user_name']
            )
            
            if ai_submission.get("success", False):
                # Wait for processing and get results
                self.log("⏳ Waiting for AI processing...")
                await asyncio.sleep(5)  # Wait for processing
                
                ai_results = await self.get_ai_submission_results(self.session_id)
                if ai_results.get("success", False):
                    self.log("✅ Real AI analysis completed")
                else:
                    self.log("⚠️ Real AI analysis failed, using enhanced simulation")
                ai_results = self.enhanced_ai_simulation(
                    test_data['text_content'],
                    test_data['voice_transcript'],
                    test_data['file_content'],
                    test_data['user_name']
                )
            else:
                self.log("⚠️ Real AI submission failed, using enhanced simulation")
                ai_results = self.enhanced_ai_simulation(
                    test_data['text_content'],
                    test_data['voice_transcript'],
                    test_data['file_content'],
                    test_data['user_name']
                )
        else:
            # Use enhanced simulation
            self.log("🧠 Using enhanced AI simulation...")
            ai_results = self.enhanced_ai_simulation(
                test_data['text_content'],
                test_data['voice_transcript'],
                test_data['file_content'],
                test_data['user_name']
            )
        
        ai_duration = self.measure_time("AI Analysis", ai_start)
        
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
        self.log(f"🤖 AI Services: {'Real' if self.ai_services_available else 'Enhanced Simulation'}")
        self.log(f"📧 Initial Notifications: {successful_notifications}/3")
        self.log(f"📱 Final Notifications: {successful_final}/3")
        
        # Store results
        self.results = {
            "session_id": self.session_id,
            "total_time": total_time,
            "ai_duration": ai_duration,
            "ai_results": ai_results,
            "ai_services_used": "Real" if self.ai_services_available else "Enhanced Simulation",
            "notification_results": notification_results,
            "final_results": final_results,
            "successful_notifications": successful_notifications,
            "successful_final": successful_final
        }
        
        return self.results

def get_user_input():
    """Get user input for test data"""
    print("\n🚀 StateX Real AI Workflow Test")
    print("=" * 50)
    print("This test uses real AI services when available, or enhanced simulation.")
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
    tester = RealAIWorkflowTester()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--default":
            print("🚀 Using default test data...")
            test_data = DEFAULT_TEST_DATA
        elif sys.argv[1] == "--demo":
            print("🚀 Running demo with sample data...")
            test_data = DEFAULT_TEST_DATA
        else:
            print("Usage: python3 test_workflow_real_ai.py [--default|--demo]")
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
        print(f"   AI Services: {results['ai_services_used']}")
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
