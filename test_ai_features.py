#!/usr/bin/env python3
"""
Test script for AI features
Tests AI assistant initialization and basic functionality
"""

import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import openai
        print("✓ OpenAI library installed")
        has_openai = True
    except ImportError:
        print("✗ OpenAI library not installed (pip install openai)")
        has_openai = False
    
    try:
        from ai_assistant import AIAssistant, HAS_OPENAI
        print(f"✓ AI Assistant module imported (HAS_OPENAI={HAS_OPENAI})")
    except ImportError as e:
        print(f"✗ Failed to import AI Assistant: {e}")
        return False
    
    try:
        from lead_processor_v2 import LeadProcessor
        print("✓ Lead Processor module imported")
    except ImportError as e:
        print(f"✗ Failed to import Lead Processor: {e}")
        return False
    
    try:
        from dialer_gui import DialerGUI
        print("✓ Dialer GUI module imported")
    except ImportError as e:
        print(f"✗ Failed to import Dialer GUI: {e}")
        return False
    
    return has_openai

def test_ai_assistant():
    """Test AI Assistant initialization"""
    print("\nTesting AI Assistant...")
    
    from ai_assistant import AIAssistant
    
    # Test without API key
    ai = AIAssistant(api_key=None)
    if not ai.enabled:
        print("✓ AI Assistant correctly disabled without API key")
    else:
        print("✗ AI Assistant should be disabled without API key")
        return False
    
    # Test with dummy API key (won't connect but should initialize)
    ai = AIAssistant(api_key="sk-test-dummy-key")
    if ai.api_key == "sk-test-dummy-key":
        print("✓ AI Assistant initialized with API key")
    else:
        print("✗ AI Assistant failed to store API key")
        return False
    
    print("✓ AI Assistant basic functionality works")
    return True

def test_lead_processor_ai():
    """Test Lead Processor with AI integration"""
    print("\nTesting Lead Processor AI integration...")
    
    from lead_processor_v2 import LeadProcessor
    from ai_assistant import AIAssistant
    
    # Test without AI
    processor = LeadProcessor(api_key="test-key", use_cache=False)
    if processor.ai_assistant is None:
        print("✓ Lead Processor works without AI assistant")
    else:
        print("✗ Lead Processor should have no AI assistant by default")
        return False
    
    # Test with AI
    ai = AIAssistant(api_key="sk-test-key")
    processor = LeadProcessor(api_key="test-key", use_cache=False, ai_assistant=ai)
    if processor.ai_assistant is not None:
        print("✓ Lead Processor accepts AI assistant")
    else:
        print("✗ Lead Processor failed to accept AI assistant")
        return False
    
    print("✓ Lead Processor AI integration works")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Features Test Suite")
    print("=" * 60)
    print()
    
    # Test imports
    has_openai = test_imports()
    
    if not has_openai:
        print("\n" + "=" * 60)
        print("WARNING: OpenAI library not installed")
        print("AI features will be disabled in the application")
        print("To enable AI features, run: pip install openai")
        print("=" * 60)
        return
    
    # Test AI Assistant
    if not test_ai_assistant():
        print("\n✗ AI Assistant tests failed")
        sys.exit(1)
    
    # Test Lead Processor integration
    if not test_lead_processor_ai():
        print("\n✗ Lead Processor AI integration tests failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print()
    print("AI features are ready to use.")
    print("Configure your OpenAI API key in the application setup.")
    print()

if __name__ == "__main__":
    main()
