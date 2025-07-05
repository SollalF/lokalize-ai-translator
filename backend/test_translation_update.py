#!/usr/bin/env python3
"""
Simple test script to demonstrate the translation update functionality.
This script shows how to use the new translation endpoints.
"""

import asyncio

from app.schemas.lokalise.translations import TranslationUpdate
from app.services.lokalise import lokalise_service


async def test_translation_operations():
    """Test the translation CRUD operations."""

    # Test project ID (replace with your actual project ID)
    project_id = "29105478684d1002288cb1.00975287"

    print("🔍 Testing Translation Operations")
    print("=" * 50)

    try:
        # 1. Get all translations
        print("\n1. Fetching all translations...")
        translations = await lokalise_service.get_translations(
            project_id=project_id,
            limit=5,  # Limit to first 5 for testing
        )
        print(f"✅ Found {len(translations)} translations")

        if translations:
            # Show first translation
            first_translation = translations[0]
            print("📝 First translation:")
            print(f"   ID: {first_translation.translation_id}")
            print(f"   Key ID: {first_translation.key_id}")
            print(f"   Language: {first_translation.language_iso}")
            print(f"   Content: {first_translation.translation}")
            print(f"   Reviewed: {first_translation.is_reviewed}")
            print(f"   Unverified: {first_translation.is_unverified}")

            # 2. Get specific translation
            print(
                f"\n2. Fetching specific translation {first_translation.translation_id}..."
            )
            specific_translation = await lokalise_service.get_translation(
                project_id=project_id, translation_id=first_translation.translation_id
            )
            print(f"✅ Retrieved translation: {specific_translation.translation}")

            # 3. Update translation (example)
            print(
                f"\n3. Example update data for translation {first_translation.translation_id}:"
            )

            # Example 1: Basic update without custom statuses (recommended for most projects)
            update_example_basic = TranslationUpdate(
                translation="Updated translation content",
                is_reviewed=True,
                is_unverified=False,
                # Note: custom_translation_statuses omitted to avoid API errors
            )
            print(
                f"📝 Basic update data: {update_example_basic.model_dump_json(indent=2)}"
            )

            # Example 2: Update with custom statuses (only if feature is enabled)
            update_example_with_custom = TranslationUpdate(
                translation="Updated translation with custom status",
                is_reviewed=True,
                is_unverified=False,
                custom_translation_statuses=[1, 2],  # Only use if feature is enabled
            )
            print(
                f"📝 Update with custom statuses: {update_example_with_custom.model_dump_json(indent=2)}"
            )
            print(
                "⚠️  Note: Custom statuses require the feature to be enabled in Lokalise project settings"
            )

            print("⚠️  Note: Actual update not performed to avoid modifying real data")

            # Uncomment the following lines to perform actual update (use basic example):
            # updated_translation = await lokalise_service.update_translation(
            #     project_id=project_id,
            #     translation_id=first_translation.translation_id,
            #     update_data=update_example_basic  # Use basic example to avoid custom status errors
            # )
            # print(f"✅ Updated translation: {updated_translation.translation}")

        else:
            print("⚠️  No translations found in project")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_translation_operations())
