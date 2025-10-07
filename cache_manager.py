#!/usr/bin/env python3
"""
Permanent Cache Manager for TrestleIQ Lead Processor
Stores API lookup results across sessions to reduce costs
"""

import json
import os
import re
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages persistent cache for API lookups"""
    
    def __init__(self, cache_file: str = "lead_processor_cache.json"):
        """
        Initialize cache manager
        
        Args:
            cache_file: Path to cache file (default: lead_processor_cache.json in program directory)
        """
        self.cache_file = cache_file
        self.cache_data = {
            "cache_version": "1.0",
            "last_updated": self._get_timestamp(),
            "lookups": {}
        }
        self.load_cache()
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_calls_saved = 0
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
    
    def normalize_phone(self, phone: str) -> str:
        """
        Normalize phone number to E.164 format for consistent cache keys
        
        Examples:
            "(415) 555-1234" → "+14155551234"
            "415-555-1234"   → "+14155551234"
            "+1-415-555-1234" → "+14155551234"
        """
        if not phone:
            return ""
        
        # Remove all non-digit characters except +
        phone_clean = re.sub(r'[^\d+]', '', str(phone))
        
        # Ensure E.164 format: +[country code][number]
        if not phone_clean.startswith('+'):
            if phone_clean.startswith('1') and len(phone_clean) == 11:
                phone_clean = '+' + phone_clean
            elif len(phone_clean) == 10:
                phone_clean = '+1' + phone_clean
            elif len(phone_clean) == 11:
                phone_clean = '+' + phone_clean
        
        return phone_clean
    
    def load_cache(self) -> bool:
        """
        Load cache from disk
        
        Returns:
            True if cache loaded successfully, False otherwise
        """
        if not os.path.exists(self.cache_file):
            logger.info(f"Cache file not found, creating new cache: {self.cache_file}")
            self.save_cache()
            return False
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # Validate cache structure
            if not isinstance(loaded_data, dict) or 'lookups' not in loaded_data:
                logger.warning("Invalid cache structure, recreating cache")
                self.save_cache()
                return False
            
            self.cache_data = loaded_data
            entry_count = len(self.cache_data.get('lookups', {}))
            logger.info(f"Cache loaded successfully: {entry_count} entries")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Cache file corrupted, recreating: {e}")
            self.save_cache()
            return False
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            return False
    
    def save_cache(self) -> bool:
        """
        Save cache to disk with atomic write
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Update timestamp
            self.cache_data['last_updated'] = self._get_timestamp()
            
            # Atomic write: write to temp file, then rename
            temp_file = self.cache_file + '.tmp'
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
            
            # Rename temp file to actual cache file (atomic on most systems)
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
            os.rename(temp_file, self.cache_file)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
            # Clean up temp file if it exists
            temp_file = self.cache_file + '.tmp'
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            return False
    
    def get_cached_lookup(self, phone: str) -> Optional[Tuple[Dict, Dict, Dict]]:
        """
        Get cached API responses and AI analysis for a phone number
        
        Args:
            phone: Phone number to lookup
        
        Returns:
            Tuple of (reverse_phone_response, reverse_address_response, ai_analysis) if cached,
            None if not found
        """
        normalized_phone = self.normalize_phone(phone)
        
        if not normalized_phone:
            return None
        
        lookups = self.cache_data.get('lookups', {})
        
        if normalized_phone in lookups:
            entry = lookups[normalized_phone]
            self.cache_hits += 1
            self.api_calls_saved += 2  # Both phone and address lookups saved
            
            logger.info(f"Cache HIT for {normalized_phone}")
            
            return (
                entry.get('reverse_phone', {}),
                entry.get('reverse_address', {}),
                entry.get('ai_analysis', {})
            )
        
        self.cache_misses += 1
        logger.info(f"Cache MISS for {normalized_phone}")
        return None
    
    def store_lookup(self, phone: str, reverse_phone_response: Dict, 
                    reverse_address_response: Dict, ai_analysis: Dict = None) -> bool:
        """
        Store successful API lookup results and AI analysis in cache
        
        Args:
            phone: Phone number
            reverse_phone_response: Complete API response from phone lookup
            reverse_address_response: Complete API response from address lookup
            ai_analysis: AI analysis results (optional)
        
        Returns:
            True if stored and saved successfully
        """
        normalized_phone = self.normalize_phone(phone)
        
        if not normalized_phone:
            return False
        
        # Only cache successful lookups (non-empty responses)
        if not reverse_phone_response and not reverse_address_response:
            logger.info(f"Skipping cache for {normalized_phone} - no data to cache")
            return False
        
        # Store in cache
        cache_entry = {
            'timestamp': self._get_timestamp(),
            'reverse_phone': reverse_phone_response,
            'reverse_address': reverse_address_response
        }
        
        # Add AI analysis if provided
        if ai_analysis:
            cache_entry['ai_analysis'] = ai_analysis
        
        self.cache_data['lookups'][normalized_phone] = cache_entry
        
        logger.info(f"Cached lookup for {normalized_phone}")
        
        # Save to disk immediately
        return self.save_cache()
    
    def update_ai_analysis(self, phone: str, ai_analysis: Dict) -> bool:
        """
        Update AI analysis for an existing cache entry
        
        Args:
            phone: Phone number
            ai_analysis: AI analysis results
        
        Returns:
            True if updated and saved successfully
        """
        normalized_phone = self.normalize_phone(phone)
        
        if not normalized_phone:
            return False
        
        lookups = self.cache_data.get('lookups', {})
        
        if normalized_phone in lookups:
            lookups[normalized_phone]['ai_analysis'] = ai_analysis
            lookups[normalized_phone]['timestamp'] = self._get_timestamp()
            
            logger.info(f"Updated AI analysis for {normalized_phone}")
            return self.save_cache()
        
        return False
    
    def clear_cache(self) -> Tuple[int, bool]:
        """
        Clear all cached entries
        
        Returns:
            Tuple of (number of entries cleared, success)
        """
        entry_count = len(self.cache_data.get('lookups', {}))
        
        self.cache_data['lookups'] = {}
        self.cache_data['last_updated'] = self._get_timestamp()
        
        success = self.save_cache()
        
        if success:
            logger.info(f"Cache cleared: {entry_count} entries removed")
        
        return entry_count, success
    
    def get_statistics(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        lookups = self.cache_data.get('lookups', {})
        entry_count = len(lookups)
        
        # Calculate file size
        file_size = 0
        if os.path.exists(self.cache_file):
            file_size = os.path.getsize(self.cache_file)
        
        # Find oldest entry
        oldest_date = None
        if lookups:
            timestamps = [entry.get('timestamp', '') for entry in lookups.values()]
            timestamps = [t for t in timestamps if t]
            if timestamps:
                oldest_date = min(timestamps)
        
        # Estimate API costs saved (assuming $0.01 per lookup, 2 lookups per entry)
        estimated_savings = self.api_calls_saved * 0.01
        
        return {
            'total_entries': entry_count,
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'oldest_entry': oldest_date,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'api_calls_saved': self.api_calls_saved,
            'estimated_savings_usd': round(estimated_savings, 2),
            'hit_rate': round(self.cache_hits / (self.cache_hits + self.cache_misses) * 100, 1) if (self.cache_hits + self.cache_misses) > 0 else 0
        }
    
    def get_cache_info_string(self) -> str:
        """Get formatted cache information string"""
        stats = self.get_statistics()
        
        info = f"Cache Statistics:\n"
        info += f"  Total Entries: {stats['total_entries']}\n"
        info += f"  File Size: {stats['file_size_mb']} MB\n"
        info += f"  Cache Hits: {stats['cache_hits']}\n"
        info += f"  Cache Misses: {stats['cache_misses']}\n"
        info += f"  Hit Rate: {stats['hit_rate']}%\n"
        info += f"  API Calls Saved: {stats['api_calls_saved']}\n"
        info += f"  Estimated Savings: ${stats['estimated_savings_usd']}\n"
        
        if stats['oldest_entry']:
            info += f"  Oldest Entry: {stats['oldest_entry']}\n"
        
        return info


def main():
    """Test cache manager"""
    logging.basicConfig(level=logging.INFO)
    
    cache = CacheManager("test_cache.json")
    
    # Test storing
    print("Testing cache storage...")
    cache.store_lookup(
        "+14155551234",
        {"id": "test1", "phone_number": "+14155551234", "owners": []},
        {"id": "test2", "current_residents": []}
    )
    
    # Test retrieval
    print("\nTesting cache retrieval...")
    result = cache.get_cached_lookup("+14155551234")
    if result:
        print("✓ Cache hit!")
        print(f"  Phone data: {result[0]}")
        print(f"  Address data: {result[1]}")
    
    # Test normalization
    print("\nTesting phone normalization...")
    test_phones = [
        "(415) 555-1234",
        "415-555-1234",
        "+1-415-555-1234",
        "4155551234"
    ]
    for phone in test_phones:
        normalized = cache.normalize_phone(phone)
        print(f"  {phone:20} → {normalized}")
    
    # Test statistics
    print("\nCache Statistics:")
    print(cache.get_cache_info_string())
    
    # Clean up
    if os.path.exists("test_cache.json"):
        os.remove("test_cache.json")
    if os.path.exists("test_cache.json.tmp"):
        os.remove("test_cache.json.tmp")


if __name__ == "__main__":
    main()
