#!/usr/bin/env python3
"""
Basic test for enhanced notification components
"""

from app.telegram_formatter import TelegramBusinessOfferFormatter
from app.models import ContactInfo, BusinessAnalysis, OfferDetails, EnhancedNotificationRequest
from datetime import datetime

def test_basic_formatting():
    """Test basic formatting functionality"""
    
    print("🧪 Testing basic Telegram formatting...")
    
    # Test basic formatting functionality
    formatter = TelegramBusinessOfferFormatter()
    
    # Create test data
    contact_info = ContactInfo(
        name='John Doe',
        contact_type='telegram',
        contact_value='123456789'
    )
    
    business_analysis = BusinessAnalysis(
        project_scope='Test e-commerce platform development with modern features',
        technology_stack=['React', 'Node.js', 'PostgreSQL'],
        timeline_estimate='8-12 weeks',
        budget_range='$30,000 - $50,000',
        risk_factors=['API integration complexity', 'Third-party dependencies'],
        market_insights='Growing market opportunity with 15% annual growth',
        recommendations=['Use modern tech stack', 'Implement mobile-first design'],
        confidence_score=0.85
    )
    
    offer_details = OfferDetails(
        project_id='test_123',
        plan_url='http://localhost:3000/plan',
        offer_url='http://localhost:3000/offer',
        deliverables=['Web application', 'Mobile app', 'Admin dashboard'],
        next_steps=['Schedule consultation', 'Review requirements', 'Sign contract']
    )
    
    request = EnhancedNotificationRequest(
        submission_id='test_sub_123',
        user_id='test_user_123',
        contact_info=contact_info,
        business_analysis=business_analysis,
        offer_details=offer_details,
        processing_summary={
            'total_processing_time': 45.2, 
            'completed_steps': 5, 
            'total_steps': 6
        }
    )
    
    # Test formatting
    template = formatter.format_business_offer(request)
    message_parts = formatter.format_message_parts(template)
    
    print('✅ Telegram formatter test successful!')
    print(f'   - Template sections: {len(template.sections)}')
    print(f'   - Message parts: {len(message_parts)}')
    print(f'   - Has keyboard: {template.inline_keyboard is not None}')
    print(f'   - First message length: {len(message_parts[0]) if message_parts else 0}')
    
    # Show sample of formatted message
    if message_parts:
        print(f'\n📄 Sample formatted message (first 300 chars):')
        print('-' * 50)
        print(message_parts[0][:300] + '...' if len(message_parts[0]) > 300 else message_parts[0])
        print('-' * 50)
    
    return True

if __name__ == "__main__":
    try:
        test_basic_formatting()
        print("\n🎉 All basic tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()