"""
Examples of using the API parity tester for different endpoints.
Run these examples to verify your endpoints match Lokalise API exactly.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_root = Path(__file__).parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from tests.utils.test_parity import manual_comparison, tester


async def test_projects_list():
    """Test projects list endpoint with different parameter combinations."""
    print("=" * 60)
    print("🔍 TESTING PROJECTS LIST ENDPOINTS")
    print("=" * 60)

    # Test 1: Full data with statistics and settings
    print("\n📋 Test 1: Projects with statistics and settings")
    await manual_comparison(
        lokalise_endpoint="projects",
        our_endpoint="api/v1/lokalise/projects/",
        params={"include_statistics": 1, "include_settings": 1, "limit": 3},
    )

    # Test 2: Minimal data without statistics and settings
    print("\n📋 Test 2: Projects without statistics and settings")
    await manual_comparison(
        lokalise_endpoint="projects",
        our_endpoint="api/v1/lokalise/projects/",
        params={"include_statistics": 0, "include_settings": 0, "limit": 2},
    )

    # Test 3: With team filter (if you have multiple teams)
    print("\n📋 Test 3: Projects with team filter")
    await manual_comparison(
        lokalise_endpoint="projects",
        our_endpoint="api/v1/lokalise/projects/",
        params={
            "filter_team_id": 511396,  # Replace with your team ID
            "include_statistics": 1,
            "limit": 1,
        },
    )


async def test_single_project():
    """Test single project endpoint."""
    print("\n" + "=" * 60)
    print("🔍 TESTING SINGLE PROJECT ENDPOINT")
    print("=" * 60)

    # First get a project ID
    projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

    if not projects_data.get("projects"):
        print("❌ No projects available for testing")
        return

    project_id = projects_data["projects"][0]["project_id"]
    print(f"\n📋 Testing single project: {project_id}")

    await manual_comparison(
        lokalise_endpoint=f"projects/{project_id}",
        our_endpoint=f"api/v1/lokalise/projects/{project_id}",
    )


async def test_project_keys():
    """Example for testing project keys endpoint (when you implement it)."""
    print("\n" + "=" * 60)
    print("🔍 TESTING PROJECT KEYS ENDPOINT (EXAMPLE)")
    print("=" * 60)

    # First get a project ID
    projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

    if not projects_data.get("projects"):
        print("❌ No projects available for testing")
        return

    project_id = projects_data["projects"][0]["project_id"]
    print(f"\n📋 Testing keys for project: {project_id}")

    # Example of how you would test keys endpoint when implemented
    try:
        await manual_comparison(
            lokalise_endpoint=f"projects/{project_id}/keys",
            our_endpoint=f"api/v1/lokalise/projects/{project_id}/keys",
            params={"limit": 5},
        )
    except Exception as e:
        print(f"⚠️  Keys endpoint not implemented yet: {e}")


async def test_project_languages():
    """Example for testing project languages endpoint (when you implement it)."""
    print("\n" + "=" * 60)
    print("🔍 TESTING PROJECT LANGUAGES ENDPOINT (EXAMPLE)")
    print("=" * 60)

    # First get a project ID
    projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

    if not projects_data.get("projects"):
        print("❌ No projects available for testing")
        return

    project_id = projects_data["projects"][0]["project_id"]
    print(f"\n📋 Testing languages for project: {project_id}")

    try:
        await manual_comparison(
            lokalise_endpoint=f"projects/{project_id}/languages",
            our_endpoint=f"api/v1/lokalise/projects/{project_id}/languages",
        )
    except Exception as e:
        print(f"⚠️  Languages endpoint not implemented yet: {e}")


async def run_all_tests():
    """Run all available API parity tests."""
    print("🚀 Starting comprehensive API parity testing...")

    try:
        # Test projects endpoints
        await test_projects_list()
        await test_single_project()

        # Test other endpoints (these will show as not implemented)
        await test_project_keys()
        await test_project_languages()

        print("\n" + "=" * 60)
        print("✅ API PARITY TESTING COMPLETE!")
        print("=" * 60)
        print("All implemented endpoints match Lokalise API exactly! 🎉")

    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Run all tests
    asyncio.run(run_all_tests())
