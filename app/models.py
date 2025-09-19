"""
Data models for enhanced Telegram notifications
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class ContactInfo(BaseModel):
    name: str
    contact_type: str  # email, telegram, whatsapp, phone
    contact_value: str
    additional_info: Optional[Dict[str, Any]] = {}

class BusinessAnalysis(BaseModel):
    project_scope: str
    technology_stack: List[str]
    timeline_estimate: str
    budget_range: str
    risk_factors: List[str]
    market_insights: str
    recommendations: List[str]
    confidence_score: Optional[float] = 0.0

class OfferDetails(BaseModel):
    project_id: str
    plan_url: str
    offer_url: str
    pricing_tiers: List[Dict[str, Any]] = []
    implementation_phases: List[Dict[str, Any]] = []
    deliverables: List[str] = []
    next_steps: List[str] = []

class AgentResult(BaseModel):
    agent_id: str
    agent_type: str
    agent_name: str
    status: str
    processing_time: float
    result_data: Dict[str, Any]
    confidence_score: float
    error_message: Optional[str] = None

class FileAnalysisSummary(BaseModel):
    file_name: str
    file_type: str
    file_size: int
    extracted_text_length: int
    key_insights: List[str]
    processing_status: str

class VoiceTranscriptionResult(BaseModel):
    duration_seconds: float
    transcript: str
    confidence_score: float
    key_topics: List[str]
    processing_status: str

class EnhancedNotificationRequest(BaseModel):
    submission_id: str
    user_id: str
    contact_info: ContactInfo
    business_analysis: Optional[BusinessAnalysis] = None
    offer_details: Optional[OfferDetails] = None
    agent_results: List[AgentResult] = []
    file_analysis_summaries: List[FileAnalysisSummary] = []
    voice_transcription: Optional[VoiceTranscriptionResult] = None
    processing_summary: Dict[str, Any] = {}
    notification_type: str = "business_offer"
    created_at: datetime = Field(default_factory=datetime.now)

class NotificationTemplate(BaseModel):
    template_name: str
    title: str
    sections: List[Dict[str, Any]]
    inline_keyboard: Optional[Dict[str, Any]] = None
    parse_mode: str = "Markdown"

class NotificationDeliveryStatus(BaseModel):
    notification_id: str
    submission_id: str
    channel: str
    status: str  # pending, sent, failed, retrying
    attempts: int = 0
    max_attempts: int = 3
    last_attempt: Optional[datetime] = None
    error_message: Optional[str] = None
    delivery_confirmation: Optional[Dict[str, Any]] = None