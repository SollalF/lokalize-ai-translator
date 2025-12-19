#!/usr/bin/env python3
"""
Debug script to check environment variable loading.
Run this from your IDE to see if environment variables are being loaded properly.
"""

import os
import sys
from pathlib import Path

print("🔍 Environment Debug Information")
print("=" * 50)

# Check Python path
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Check if .env file exists
env_file = Path(".env")
print(f"\n📁 .env file exists: {env_file.exists()}")
if env_file.exists():
    print(f"📁 .env file path: {env_file.absolute()}")

# Try to load .env file
print("\n🔄 Attempting to load .env file...")
try:
    from dotenv import load_dotenv

    load_dotenv()
    print("✅ Successfully loaded .env file")
except ImportError:
    print("❌ python-dotenv not available")
except Exception as e:
    print(f"❌ Error loading .env: {e}")

# Check environment variables
print("\n🔑 Environment Variables:")
lok_token = os.getenv("LOKALISE_API_TOKEN")
print(f"LOKALISE_API_TOKEN: {'✅ Set' if lok_token else '❌ Not set'}")
if lok_token:
    print(f"  Token preview: {lok_token[:10]}...")

# Check other important vars
important_vars = [
    "API_HOST",
    "API_PORT",
    "ENVIRONMENT",
    "SECRET_KEY",
    "GEMINI_API_KEY",
    "LOG_LEVEL",
]

for var in important_vars:
    value = os.getenv(var)
    status = "✅ Set" if value else "❌ Not set"
    print(f"{var}: {status}")

# Try to import app settings
print("\n🏗️  App Configuration:")
try:
    from app.core.config import get_settings

    settings = get_settings()
    print("✅ Successfully imported app settings")

    # Check if settings has the token
    if hasattr(settings, "LOKALISE_API_TOKEN"):
        settings_token = settings.LOKALISE_API_TOKEN
        print(
            f"Settings LOKALISE_API_TOKEN: {'✅ Set' if settings_token else '❌ Not set'}"
        )
        if settings_token:
            print(f"  Token preview: {settings_token[:10]}...")
    else:
        print("❌ Settings object doesn't have LOKALISE_API_TOKEN attribute")

except ImportError as e:
    print(f"❌ Could not import app settings: {e}")
except Exception as e:
    print(f"❌ Error with app settings: {e}")

print("\n" + "=" * 50)
print("💡 If environment variables are not set, check your IDE configuration.")
print("💡 Make sure your IDE is using the virtual environment Python interpreter.")
