#!/usr/bin/env python3
"""
Test script for glossary translation flow with detailed logging.

Usage:
    python test_glossary_translation.py

This script will test the glossary translation endpoint with sample data
and show all debug logging to help identify issues.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.core.logging import setup_logging
from app.services.glossary_aware_translation import glossary_aware_translation_service


async def test_glossary_translation():
    """Test the glossary translation flow with debug logging."""

    # Setup detailed logging
    setup_logging()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Test data
    test_cases = [
        {
            "name": "Simple test with 'crypto dust'",
            "source_text": "crypto dust",
            "source_lang": "en",
            "target_lang": "es_419",
            "project_id": "29105478684d1002288cb1.00975287",
        },
        {
            "name": "Test without project_id (regular translation)",
            "source_text": "crypto dust",
            "source_lang": "en",
            "target_lang": "es_419",
            "project_id": None,
        },
        {
            "name": "Test with longer text",
            "source_text": "The crypto dust in my wallet is worth very little.",
            "source_lang": "en",
            "target_lang": "fr",
            "project_id": "29105478684d1002288cb1.00975287",
        },
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\n{'=' * 80}")
        print(f"TEST CASE {i + 1}: {test_case['name']}")
        print(f"{'=' * 80}")

        try:
            result = await glossary_aware_translation_service.translate_with_glossary(
                source_text=test_case["source_text"],
                source_lang=test_case["source_lang"],
                target_lang=test_case["target_lang"],
                project_id=test_case["project_id"],
                preserve_forbidden_terms=True,
                translate_allowed_terms=True,
            )

            print(f"\n✅ TEST CASE {i + 1} COMPLETED SUCCESSFULLY")
            print(f"Result keys: {list(result.keys())}")
            print(f"Translated text: '{result['translated_text']}'")
            print(f"Verification success: {result['verification_results']['success']}")

        except Exception as e:
            print(f"\n❌ TEST CASE {i + 1} FAILED")
            print(f"Error: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback

            traceback.print_exc()

        print(f"\n{'=' * 80}")
        print(f"END OF TEST CASE {i + 1}")
        print(f"{'=' * 80}\n")


if __name__ == "__main__":
    print("Starting Glossary Translation Debug Test")
    print("=" * 80)

    asyncio.run(test_glossary_translation())

    print("\nTest completed!")
