#!/usr/bin/env python3
"""
AI Assistant for Passion Of Rugs Advanced Dialer v4.1
Provides address correction and intelligent person filtering using OpenAI GPT-5 nano
(Cheapest option: $0.025/1M input tokens, $0.20/1M output tokens - Batch tier)
"""

import json
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Try to import OpenAI
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    logger.warning("OpenAI not installed - AI features disabled")


class AIAssistant:
    """AI-powered address correction and person filtering"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-5-nano"):
        self.api_key = api_key
        self.model = model  # Default: gpt-5-nano (cheapest option)
        self.enabled = HAS_OPENAI and bool(api_key)
        
        if self.enabled:
            self.client = openai.OpenAI(api_key=api_key)
            logger.info(f"AI Assistant initialized with {self.model}")
        else:
            self.client = None
            logger.warning("AI Assistant disabled - missing API key or OpenAI library")
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test OpenAI API connection"""
        if not self.enabled:
            return False, "OpenAI library not installed or API key missing"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_completion_tokens=5
            )
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def correct_address(self, street_line_1: str, street_line_2: str, city: str, 
                       state_code: str, postal_code: str) -> Optional[Dict]:
        """
        Correct malformed address using AI
        Returns corrected address dict or None if AI fails
        """
        if not self.enabled:
            return None
        
        prompt = f"""You are an address validation expert for US addresses. The following address failed validation from the Trestle Reverse Address API.

Original Address Data:
Street Line 1: {street_line_1 or "NOT PROVIDED"}
Street Line 2: {street_line_2 or "NOT PROVIDED"}
City: {city or "NOT PROVIDED"}
State: {state_code or "NOT PROVIDED"}
Postal Code: {postal_code or "NOT PROVIDED"}

API Requirements (Trestle Reverse Address API 3.1):
- street_line_1: Required, max 1000 chars
- city: Required, max 500 chars
- state_code: Required, max 100 chars (2-letter state abbreviation)
- postal_code: Required, max 100 chars (5-digit ZIP or ZIP+4)
- street_line_2: Optional (for apartments/suites)
- country_code: Optional (default US)

Common address issues to fix:
1. Abbreviated street types (St→Street, Ave→Avenue, Blvd→Boulevard, Rd→Road, Ln→Lane, Dr→Drive)
2. Missing or misspelled state codes (must be 2-letter: CA, NY, TX, etc.)
3. Incomplete ZIP codes or wrong format
4. Missing city names
5. Typos, OCR errors, extra spaces
6. Missing apartment/unit numbers when "Apt", "#", "Unit" appears in street
7. Street numbers at end instead of beginning

Correct this address to match API requirements. Return ONLY valid JSON:

{{
  "street_line_1": "corrected street with number at start",
  "street_line_2": "unit/apt if applicable or empty string",
  "city": "corrected city name",
  "state_code": "XX",
  "postal_code": "XXXXX",
  "country_code": "US",
  "correction_reasoning": "what was fixed"
}}"""
        
        try:
            # First try with json_object format
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    max_completion_tokens=300
                )
            except Exception as format_error:
                logger.warning(f"JSON format not supported, trying without: {format_error}")
                # Fallback without response_format
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=300
                )
            
            # Debug: Log the raw response
            raw_content = response.choices[0].message.content
            logger.info(f"AI raw response: '{raw_content}'")
            
            if not raw_content or raw_content.strip() == "":
                logger.error("AI returned empty response")
                return None
            
            # Try to extract JSON from the response
            content = raw_content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            logger.info(f"AI address correction: {result.get('correction_reasoning', 'No reasoning')}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"AI returned invalid JSON: {e}")
            logger.error(f"Raw response was: '{raw_content if 'raw_content' in locals() else 'No response'}'")
            return None
        except Exception as e:
            logger.error(f"AI address correction failed: {e}")
            return None
    
    def filter_and_rank_contacts(self, original_name: str, original_phone: str, 
                                 original_address: str, reverse_phone_response: Dict,
                                 reverse_address_response: Dict) -> Optional[Dict]:
        """
        Intelligently filter and rank contacts to find the original customer
        Returns structured results with confidence scores and insights
        """
        if not self.enabled:
            return None
        
        prompt = f"""You are a customer data analyst. Match the original customer with their current contact information.

ORIGINAL CUSTOMER (from 2015 purchase records):
Name: {original_name}
Phone: {original_phone}
Address: {original_address}

REVERSE PHONE API RESPONSE:
{json.dumps(reverse_phone_response, indent=2)}

REVERSE ADDRESS API RESPONSE:
{json.dumps(reverse_address_response, indent=2)}

Task: Identify phone numbers for the ORIGINAL CUSTOMER ONLY (not relatives unless specified).

Instructions:
1. Find exact name matches (first + last) from both API responses
2. Combine all phone numbers for that person (deduplicate)
3. Prioritize mobile > landline > VOIP
4. Identify close relatives (spouse, same last name at same address)
5. Calculate confidence based on:
   - Name match strength (exact = 100%, partial = lower)
   - Address continuity (still at address vs moved)
   - Phone type (mobile higher than VOIP)
   - Data recency (link_to_address_start_date)

Return ONLY this JSON structure:

{{
  "primary_matches": [
    {{
      "name": "exact customer name",
      "phone": "+1XXXXXXXXXX",
      "phone_type": "Mobile|Landline|FixedVOIP|NonFixedVOIP",
      "carrier": "carrier name",
      "source": "Reverse Phone|Reverse Address|Both",
      "current_address": "full address if available",
      "confidence_score": 95,
      "confidence_level": "High|Medium|Low",
      "reasoning": "why this is the customer",
      "priority": 1
    }}
  ],
  "related_contacts": [
    {{
      "name": "relative name",
      "relationship": "Spouse|Same Last Name|Associated Person",
      "phone": "+1XXXXXXXXXX",
      "phone_type": "Mobile|Landline",
      "confidence_score": 70,
      "reasoning": "same address, listed as spouse",
      "priority": 2
    }}
  ],
  "insights": {{
    "acceptance_probability": 85,
    "acceptance_reasoning": "exact match, current mobile, active at address",
    "best_time_to_call": "Weekday evenings|Business hours|Anytime",
    "recommended_first_contact": "+1XXXXXXXXXX",
    "address_changes": 1,
    "time_at_current_address": "5 years",
    "additional_notes": "moved from Springfield to Seattle in 2020"
  }}
}}

IMPORTANT: Only include people clearly connected to original customer. Exclude unrelated residents."""
        
        try:
            # First try with json_object format
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    max_completion_tokens=1500
                )
            except Exception as format_error:
                logger.warning(f"JSON format not supported, trying without: {format_error}")
                # Fallback without response_format
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=1500
                )
            
            # Debug: Log the raw response
            raw_content = response.choices[0].message.content
            logger.info(f"AI raw response: '{raw_content}'")
            
            if not raw_content or raw_content.strip() == "":
                logger.error("AI returned empty response")
                return None
            
            # Try to extract JSON from the response
            content = raw_content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            logger.info(f"AI filtering complete: {len(result.get('primary_matches', []))} primary matches")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"AI returned invalid JSON: {e}")
            logger.error(f"Raw response was: '{raw_content if 'raw_content' in locals() else 'No response'}'")
            return None
        except Exception as e:
            logger.error(f"AI filtering failed: {e}")
            return None
