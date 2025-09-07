#!/usr/bin/env python3
"""
StateX Free AI Workflow Test Script

This script uses FREE AI services for testing:
1. Ollama (Local LLM) - Primary option
2. Hugging Face Inference API - Secondary option
3. Mock AI Service - Fallback option

Usage:
    python3 test_workflow_free_ai.py                    # Interactive mode
    python3 test_workflow_free_ai.py --default          # Use default test data
    python3 test_workflow_free_ai.py --demo             # Run demo with sample data
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
OLLAMA_URL = "http://localhost:11434"  # Ollama default port
HUGGINGFACE_URL = "https://api-inference.huggingface.co/models"

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

class FreeAIWorkflowTester:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = None
        self.results = {}
        self.ai_service_used = "none"
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def measure_time(self, operation: str, start_time: float):
        """Measure and log operation time"""
        duration = time.time() - start_time
        self.log(f"{operation} completed in {duration:.2f} seconds")
        return duration
        
    async def check_ai_services(self) -> str:
        """Check which AI services are available"""
        self.log("🔍 Checking free AI services availability...")
        
        # Check Ollama (Local LLM)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{OLLAMA_URL}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        models = await response.json()
                        if models.get("models"):
                            self.log("✅ Ollama (Local LLM) is available")
                            return "ollama"
        except Exception as e:
            self.log(f"❌ Ollama not available: {e}", "ERROR")
        
        # Check Hugging Face (Free API)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{HUGGINGFACE_URL}/microsoft/DialoGPT-medium", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        self.log("✅ Hugging Face API is available")
                        return "huggingface"
        except Exception as e:
            self.log(f"❌ Hugging Face API not available: {e}", "ERROR")
        
        self.log("⚠️ No free AI services available - will use mock AI service")
        return "mock"
        
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
    
    async def analyze_with_ollama(self, text_content: str, user_name: str) -> Dict[str, Any]:
        """Analyze using Ollama (Local LLM)"""
        self.log("🤖 Analyzing with Ollama (Local LLM)...")
        
        # Create a comprehensive prompt for business analysis
        prompt = f"""Analyze this business request and provide a comprehensive analysis:

User: {user_name}
Request: {text_content}

Please provide:
1. Business type and industry
2. Key pain points
3. Business opportunities
4. Technical recommendations
5. Next steps
6. Budget estimate
7. Timeline estimate

Format as JSON with these fields:
- business_type
- pain_points (array)
- opportunities (array with name, description, potential, timeline)
- technical_recommendations (object with frontend, backend, integrations)
- next_steps (array with action, priority, timeline)
- budget_estimate (object with development, infrastructure, maintenance)
- confidence (0-1)
- summary (string)
"""
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": "llama2:7b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                }
                
                async with session.post(
                    f"{OLLAMA_URL}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_response = result.get("response", "")
                        
                        # Try to parse JSON response
                        try:
                            # Extract JSON from response
                            json_start = ai_response.find('{')
                            json_end = ai_response.rfind('}') + 1
                            if json_start != -1 and json_end != -1:
                                json_str = ai_response[json_start:json_end]
                                analysis = json.loads(json_str)
                            else:
                                # Fallback to text parsing
                                analysis = self.parse_text_response(ai_response, user_name)
                        except:
                            analysis = self.parse_text_response(ai_response, user_name)
                        
                        self.log("✅ Ollama analysis completed")
                        return analysis
                    else:
                        error_text = await response.text()
                        self.log(f"❌ Ollama analysis failed: {response.status} - {error_text}", "ERROR")
                        return self.mock_ai_analysis(text_content, user_name)
        except Exception as e:
            self.log(f"❌ Ollama error: {str(e)}", "ERROR")
            return self.mock_ai_analysis(text_content, user_name)
    
    async def analyze_with_huggingface(self, text_content: str, user_name: str) -> Dict[str, Any]:
        """Analyze using Hugging Face API"""
        self.log("🤖 Analyzing with Hugging Face API...")
        
        # Use a text generation model
        model = "microsoft/DialoGPT-medium"
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "inputs": f"Analyze this business request: {text_content[:500]}",
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.7
                    }
                }
                
                async with session.post(
                    f"{HUGGINGFACE_URL}/{model}",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_response = result[0].get("generated_text", "")
                        
                        # Parse the response
                        analysis = self.parse_text_response(ai_response, user_name)
                        self.log("✅ Hugging Face analysis completed")
                        return analysis
                    else:
                        error_text = await response.text()
                        self.log(f"❌ Hugging Face analysis failed: {response.status} - {error_text}", "ERROR")
                        return self.mock_ai_analysis(text_content, user_name)
        except Exception as e:
            self.log(f"❌ Hugging Face error: {str(e)}", "ERROR")
            return self.mock_ai_analysis(text_content, user_name)
    
    def mock_ai_analysis(self, text_content: str, user_name: str) -> Dict[str, Any]:
        """Mock AI analysis for testing"""
        self.log("🤖 Using mock AI analysis...")
        
        # Simulate processing time
        time.sleep(2)
        
        # Generate realistic analysis based on content
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
            if any(keyword in text_content.lower() for keyword in keywords):
                detected_business = business_type
                break
        
        return {
            "business_type": detected_business,
            "summary": f"User {user_name} wants to create a digital solution for their {detected_business} business, focusing on automation and customer experience.",
            "pain_points": [
                "Manual processes and workflows",
                "Customer communication challenges",
                "Data management and tracking",
                "Integration between systems"
            ],
            "opportunities": [
                {
                    "name": "Digital Platform Development",
                    "description": f"Comprehensive {detected_business} management platform",
                    "potential": "High",
                    "timeline": "3-6 months"
                },
                {
                    "name": "Mobile Application",
                    "description": "Native mobile app for staff and customers",
                    "potential": "High",
                    "timeline": "2-4 months"
                },
                {
                    "name": "Process Automation",
                    "description": "Automate manual processes and workflows",
                    "potential": "Medium",
                    "timeline": "1-3 months"
                }
            ],
            "technical_recommendations": {
                "frontend": ["React/Next.js", "TypeScript", "Responsive design"],
                "backend": ["Node.js/Python", "PostgreSQL", "RESTful API"],
                "integrations": ["Payment processing", "SMS/Email", "Calendar sync", "Analytics"]
            },
            "next_steps": [
                {
                    "action": f"Conduct {detected_business} market research",
                    "priority": "High",
                    "timeline": "1-2 weeks"
                },
                {
                    "action": "Develop MVP prototype",
                    "priority": "High",
                    "timeline": "4-8 weeks"
                },
                {
                    "action": "Create technical architecture",
                    "priority": "Medium",
                    "timeline": "2-3 weeks"
                }
            ],
            "budget_estimate": {
                "development": "$15,000 - $35,000",
                "infrastructure": "$200 - $500/month",
                "maintenance": "$1,000 - $2,000/month"
            },
            "confidence": 0.85,
            "ai_service": "Mock AI Service"
        }
    
    def parse_text_response(self, text: str, user_name: str) -> Dict[str, Any]:
        """Parse text response from AI into structured format"""
        # This is a simplified parser - in production you'd want more sophisticated parsing
        return {
            "business_type": "general",
            "summary": f"AI Analysis for {user_name}: {text[:200]}...",
            "pain_points": ["Manual processes", "Customer communication", "Data management"],
            "opportunities": [
                {
                    "name": "Digital Transformation",
                    "description": "Modernize business operations",
                    "potential": "High",
                    "timeline": "3-6 months"
                }
            ],
            "technical_recommendations": {
                "frontend": ["React/Next.js", "TypeScript"],
                "backend": ["Node.js", "PostgreSQL"],
                "integrations": ["Payment processing", "Notifications"]
            },
            "next_steps": [
                {
                    "action": "Market research",
                    "priority": "High",
                    "timeline": "1-2 weeks"
                },
                {
                    "action": "Prototype development",
                    "priority": "High",
                    "timeline": "4-8 weeks"
                }
            ],
            "budget_estimate": {
                "development": "$15,000 - $35,000",
                "infrastructure": "$200 - $500/month",
                "maintenance": "$1,000 - $2,000/month"
            },
            "confidence": 0.8,
            "ai_service": "Text Parser"
        }
    
    def generate_ai_summary(self, analysis_results: Dict[str, Any], user_name: str) -> str:
        """Generate AI analysis summary for notification"""
        summary = f"""🤖 *AI Analysis Complete for {user_name}*

📋 *Project Summary:*
{analysis_results['summary']}

🔍 *Business Type:*
{analysis_results['business_type'].title()}

⚠️ *Current Pain Points:*
"""
        
        # Add pain points
        for point in analysis_results['pain_points']:
            summary += f"• {point}\n"
        
        # Add business opportunities
        summary += f"\n💡 *Business Opportunities:*\n"
        for opp in analysis_results['opportunities']:
            summary += f"• {opp['name']} - {opp['potential']} potential ({opp['timeline']})\n"
        
        # Add technical recommendations
        summary += f"\n🔧 *Technical Recommendations:*\n"
        summary += f"• Frontend: {', '.join(analysis_results['technical_recommendations']['frontend'])}\n"
        summary += f"• Backend: {', '.join(analysis_results['technical_recommendations']['backend'])}\n"
        summary += f"• Integrations: {', '.join(analysis_results['technical_recommendations']['integrations'])}\n"
        
        # Add action items
        summary += f"\n📝 *Next Steps:*\n"
        for item in analysis_results['next_steps']:
            summary += f"• {item['action']} ({item['timeline']})\n"
        
        # Add budget estimate
        summary += f"\n💰 *Budget Estimate:*\n"
        summary += f"• Development: {analysis_results['budget_estimate']['development']}\n"
        summary += f"• Infrastructure: {analysis_results['budget_estimate']['infrastructure']}\n"
        summary += f"• Maintenance: {analysis_results['budget_estimate']['maintenance']}\n"
        
        summary += f"\n🎯 *Confidence:* {analysis_results['confidence']:.1%}"
        summary += f"\n🤖 *AI Service:* {analysis_results.get('ai_service', 'Unknown')}"
        
        return summary
    
    async def run_complete_workflow(self, test_data: Dict[str, Any]):
        """Run the complete workflow test"""
        self.start_time = time.time()
        self.log("🚀 Starting StateX Free AI Workflow Test")
        self.log("=" * 60)
        
        # Check AI services availability
        self.ai_service_used = await self.check_ai_services()
        
        # Step 1: Send initial confirmation notifications
        self.log("📧 Step 1: Sending initial confirmation notifications")
        confirmation_message = f"""Hello {test_data['user_name']}!

Thank you for your submission! We've received your project details:
• Text description: {len(test_data['text_content'])} characters
• Voice transcript: {len(test_data['voice_transcript'])} characters  
• File content: {len(test_data['file_content'])} characters

Our FREE AI agents are now analyzing your requirements. We'll contact you via Telegram with the analysis results shortly.

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
        
        if self.ai_service_used == "ollama":
            ai_results = await self.analyze_with_ollama(combined_text, test_data["user_name"])
        elif self.ai_service_used == "huggingface":
            ai_results = await self.analyze_with_huggingface(combined_text, test_data["user_name"])
        else:
            ai_results = self.mock_ai_analysis(combined_text, test_data["user_name"])
        
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
        self.log(f"🤖 AI Service Used: {self.ai_service_used.upper()}")
        self.log(f"📧 Initial Notifications: {successful_notifications}/3")
        self.log(f"📱 Final Notifications: {successful_final}/3")
        
        # Store results
        self.results = {
            "session_id": self.session_id,
            "total_time": total_time,
            "ai_duration": ai_duration,
            "ai_results": ai_results,
            "ai_service_used": self.ai_service_used,
            "notification_results": notification_results,
            "final_results": final_results,
            "successful_notifications": successful_notifications,
            "successful_final": successful_final
        }
        
        return self.results

def get_user_input():
    """Get user input for test data"""
    print("\n🚀 StateX Free AI Workflow Test")
    print("=" * 50)
    print("This test uses FREE AI services (Ollama, Hugging Face, or Mock)")
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
    tester = FreeAIWorkflowTester()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--default":
            print("🚀 Using default test data...")
            test_data = DEFAULT_TEST_DATA
        elif sys.argv[1] == "--demo":
            print("🚀 Running demo with sample data...")
            test_data = DEFAULT_TEST_DATA
        else:
            print("Usage: python3 test_workflow_free_ai.py [--default|--demo]")
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
        print(f"   AI Service: {results['ai_service_used'].upper()}")
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
