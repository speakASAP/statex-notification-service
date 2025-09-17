"""
Enhanced Telegram message formatter for business offers
"""

from typing import Dict, Any, List, Optional
from .models import (
    EnhancedNotificationRequest, BusinessAnalysis, OfferDetails,
    AgentResult, FileAnalysisSummary, VoiceTranscriptionResult,
    NotificationTemplate
)
import json

class TelegramBusinessOfferFormatter:
    """Formats business analysis results into rich Telegram messages"""
    
    def __init__(self):
        self.max_message_length = 4096  # Telegram message limit
        self.max_section_length = 800   # Max length per section to avoid truncation
    
    def format_business_offer(self, request: EnhancedNotificationRequest) -> NotificationTemplate:
        """Format complete business offer notification"""
        
        # Build message sections
        sections = []
        
        # Header section
        sections.append(self._create_header_section(request))
        
        # Customer information section
        sections.append(self._create_customer_info_section(request.contact_info))
        
        # Business analysis section
        if request.business_analysis:
            sections.append(self._create_business_analysis_section(request.business_analysis))
        
        # Agent results summary
        if request.agent_results:
            sections.append(self._create_agent_results_section(request.agent_results))
        
        # File analysis section
        if request.file_analysis_summaries:
            sections.append(self._create_file_analysis_section(request.file_analysis_summaries))
        
        # Voice transcription section
        if request.voice_transcription:
            sections.append(self._create_voice_transcription_section(request.voice_transcription))
        
        # Offer details section
        if request.offer_details:
            sections.append(self._create_offer_details_section(request.offer_details))
        
        # Processing summary section
        sections.append(self._create_processing_summary_section(request.processing_summary))
        
        # Footer section
        sections.append(self._create_footer_section())
        
        # Create inline keyboard
        inline_keyboard = self._create_inline_keyboard(request.offer_details)
        
        return NotificationTemplate(
            template_name="business_offer",
            title="🚀 StateX Business Analysis Complete",
            sections=sections,
            inline_keyboard=inline_keyboard,
            parse_mode="Markdown"
        )
    
    def _create_header_section(self, request: EnhancedNotificationRequest) -> Dict[str, Any]:
        """Create header section with submission overview"""
        return {
            "type": "header",
            "content": f"""🚀 *StateX Business Analysis Complete*

📋 *Submission ID:* `{request.submission_id}`
👤 *Customer:* {request.contact_info.name}
📅 *Processed:* {request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
🎯 *Analysis Type:* Multi-Agent Business Intelligence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        }
    
    def _create_customer_info_section(self, contact_info) -> Dict[str, Any]:
        """Create customer information section"""
        content = f"""👤 *Customer Information*

📝 *Name:* {contact_info.name}
📞 *Contact Type:* {contact_info.contact_type.title()}
📧 *Contact Value:* `{contact_info.contact_value}`"""
        
        if contact_info.additional_info:
            content += f"\n📋 *Additional Info:* {json.dumps(contact_info.additional_info, indent=2)}"
        
        return {
            "type": "customer_info",
            "content": content
        }
    
    def _create_business_analysis_section(self, analysis: BusinessAnalysis) -> Dict[str, Any]:
        """Create business analysis section"""
        
        # Format technology stack
        tech_stack = ", ".join(analysis.technology_stack) if analysis.technology_stack else "Not specified"
        
        # Format risk factors
        risk_factors = "\n".join([f"  • {risk}" for risk in analysis.risk_factors]) if analysis.risk_factors else "  • No significant risks identified"
        
        # Format recommendations
        recommendations = "\n".join([f"  • {rec}" for rec in analysis.recommendations]) if analysis.recommendations else "  • Standard implementation approach recommended"
        
        # Format confidence score
        confidence_score = f"{analysis.confidence_score:.1%}" if analysis.confidence_score else "N/A"
        
        content = f"""🧠 *AI Business Analysis*

🎯 *Project Scope:*
{self._truncate_text(analysis.project_scope, 200)}

💻 *Technology Stack:* {tech_stack}

⏱️ *Timeline Estimate:* {analysis.timeline_estimate}

💰 *Budget Range:* {analysis.budget_range}

⚠️ *Risk Factors:*
{risk_factors}

📈 *Market Insights:*
{self._truncate_text(analysis.market_insights, 200)}

💡 *Recommendations:*
{recommendations}

🎯 *Confidence Score:* {confidence_score}"""
        
        return {
            "type": "business_analysis",
            "content": content
        }
    
    def _create_agent_results_section(self, agent_results: List[AgentResult]) -> Dict[str, Any]:
        """Create agent processing results section"""
        
        successful_agents = [a for a in agent_results if a.status == "completed"]
        failed_agents = [a for a in agent_results if a.status == "failed"]
        
        content = f"""🤖 *AI Agent Processing Results*

✅ *Successful Agents:* {len(successful_agents)}/{len(agent_results)}
❌ *Failed Agents:* {len(failed_agents)}
⏱️ *Total Processing Time:* {sum(a.processing_time for a in agent_results):.1f}s

*Agent Details:*"""
        
        for agent in agent_results:
            status_emoji = "✅" if agent.status == "completed" else "❌"
            confidence = f" ({agent.confidence_score:.1%})" if agent.confidence_score > 0 else ""
            
            content += f"""
{status_emoji} *{agent.agent_name}*: {agent.processing_time:.1f}s{confidence}"""
            
            if agent.error_message and agent.status == "failed":
                content += f"\n   ⚠️ Error: {self._truncate_text(agent.error_message, 100)}"
        
        return {
            "type": "agent_results",
            "content": content
        }
    
    def _create_file_analysis_section(self, file_summaries: List[FileAnalysisSummary]) -> Dict[str, Any]:
        """Create file analysis section"""
        
        content = f"""📁 *File Analysis Summary*

📊 *Files Processed:* {len(file_summaries)}

*File Details:*"""
        
        for file_summary in file_summaries:
            status_emoji = "✅" if file_summary.processing_status == "completed" else "❌"
            file_size_mb = file_summary.file_size / (1024 * 1024)
            
            content += f"""
{status_emoji} *{file_summary.file_name}*
   📄 Type: {file_summary.file_type} | Size: {file_size_mb:.1f}MB
   📝 Extracted: {file_summary.extracted_text_length} characters"""
            
            if file_summary.key_insights:
                insights = ", ".join(file_summary.key_insights[:3])  # Show first 3 insights
                content += f"\n   💡 Key Insights: {self._truncate_text(insights, 100)}"
        
        return {
            "type": "file_analysis",
            "content": content
        }
    
    def _create_voice_transcription_section(self, voice_result: VoiceTranscriptionResult) -> Dict[str, Any]:
        """Create voice transcription section"""
        
        content = f"""🎤 *Voice Analysis Results*

⏱️ *Duration:* {voice_result.duration_seconds:.1f} seconds
🎯 *Confidence:* {voice_result.confidence_score:.1%}
📝 *Status:* {voice_result.processing_status.title()}

*Transcript:*
"{self._truncate_text(voice_result.transcript, 300)}"

*Key Topics:*"""
        
        if voice_result.key_topics:
            topics = ", ".join(voice_result.key_topics)
            content += f"\n{self._truncate_text(topics, 200)}"
        else:
            content += "\nNo specific topics identified"
        
        return {
            "type": "voice_transcription",
            "content": content
        }
    
    def _create_offer_details_section(self, offer_details: OfferDetails) -> Dict[str, Any]:
        """Create offer details section"""
        
        content = f"""💼 *Business Offer Details*

🆔 *Project ID:* `{offer_details.project_id}`

🔗 *Project Links:*
📋 [View Project Plan]({offer_details.plan_url})
💰 [View Detailed Offer]({offer_details.offer_url})"""
        
        if offer_details.pricing_tiers:
            content += f"\n\n💰 *Pricing Tiers:* {len(offer_details.pricing_tiers)} options available"
        
        if offer_details.implementation_phases:
            content += f"\n📅 *Implementation Phases:* {len(offer_details.implementation_phases)} phases planned"
        
        if offer_details.deliverables:
            deliverables = "\n".join([f"  • {d}" for d in offer_details.deliverables[:5]])  # Show first 5
            content += f"\n\n📦 *Key Deliverables:*\n{deliverables}"
            if len(offer_details.deliverables) > 5:
                content += f"\n  • ... and {len(offer_details.deliverables) - 5} more"
        
        if offer_details.next_steps:
            next_steps = "\n".join([f"  • {step}" for step in offer_details.next_steps[:3]])  # Show first 3
            content += f"\n\n🚀 *Next Steps:*\n{next_steps}"
        
        return {
            "type": "offer_details",
            "content": content
        }
    
    def _create_processing_summary_section(self, processing_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Create processing summary section"""
        
        total_time = processing_summary.get("total_processing_time", 0)
        completed_steps = processing_summary.get("completed_steps", 0)
        total_steps = processing_summary.get("total_steps", 0)
        
        # Calculate success rate
        success_rate = f"{(completed_steps/total_steps*100):.1f}%" if total_steps > 0 else "N/A"
        
        content = f"""📊 *Processing Summary*

⏱️ *Total Processing Time:* {total_time:.1f} seconds
✅ *Completed Steps:* {completed_steps}/{total_steps}
📈 *Success Rate:* {success_rate}

🔄 *Workflow Status:* Complete"""
        
        return {
            "type": "processing_summary",
            "content": content
        }
    
    def _create_footer_section(self) -> Dict[str, Any]:
        """Create footer section"""
        return {
            "type": "footer",
            "content": """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 *StateX AI Development Services*
🌐 [statex.cz](https://statex.cz)
📧 contact@statex.cz

*Ready to bring your project to life?*"""
        }
    
    def _create_inline_keyboard(self, offer_details: Optional[OfferDetails]) -> Optional[Dict[str, Any]]:
        """Create inline keyboard with action buttons"""
        
        if not offer_details:
            return {
                "inline_keyboard": [
                    [
                        {
                            "text": "📊 View Dashboard",
                            "url": "http://localhost:3000/dashboard"
                        }
                    ],
                    [
                        {
                            "text": "🚀 Request New Analysis",
                            "url": "http://localhost:3000/contact"
                        }
                    ]
                ]
            }
        
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "📋 View Project Plan",
                        "url": offer_details.plan_url
                    },
                    {
                        "text": "💰 View Offer Details",
                        "url": offer_details.offer_url
                    }
                ],
                [
                    {
                        "text": "📊 View Dashboard",
                        "url": "http://localhost:3000/dashboard"
                    }
                ],
                [
                    {
                        "text": "🚀 Request New Analysis",
                        "url": "http://localhost:3000/contact"
                    },
                    {
                        "text": "💬 Contact Sales",
                        "url": "https://t.me/statex_support"
                    }
                ]
            ]
        }
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def format_message_parts(self, template: NotificationTemplate) -> List[str]:
        """Split template into multiple messages if needed"""
        
        # Combine all sections into a single message first
        full_message = f"{template.title}\n\n"
        
        for section in template.sections:
            full_message += section["content"] + "\n\n"
        
        # If message fits in single Telegram message, return as is
        if len(full_message) <= self.max_message_length:
            return [full_message.strip()]
        
        # Split into multiple messages
        messages = []
        current_message = template.title + "\n\n"
        
        for section in template.sections:
            section_content = section["content"] + "\n\n"
            
            # If adding this section would exceed limit, start new message
            if len(current_message + section_content) > self.max_message_length:
                messages.append(current_message.strip())
                current_message = section_content
            else:
                current_message += section_content
        
        # Add remaining content
        if current_message.strip():
            messages.append(current_message.strip())
        
        return messages