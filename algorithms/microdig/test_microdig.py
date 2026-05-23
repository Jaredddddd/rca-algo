"""
Test script for the MicroDig package with new Polars data format.

This script tests the integration of all MicroDig components.
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add src directory to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


def test_imports():
    """Test if all MicroDig components can be imported"""
    logger.info("Testing MicroDig imports...")

    try:
        # Test main package import
        import microdig

        logger.info("✓ Main microdig package imported successfully")

        # Test individual component imports
        from microdig import DataLoader

        logger.info("✓ DataLoader imported successfully")

        from microdig import MicroDigAdapter

        logger.info("✓ MicroDigAdapter imported successfully")

        from microdig import microdig_analysis

        logger.info("✓ microdig_analysis function imported successfully")

        from microdig import MicroDig

        logger.info("✓ MicroDig platform class imported successfully")

        from microdig import cli_app

        logger.info("✓ CLI app imported successfully")

        logger.info("All imports successful!")
        return True

    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return False


def test_data_loader_init():
    """Test if DataLoader can be initialized"""
    logger.info("Testing DataLoader initialization...")

    try:
        from microdig import DataLoader

        # Test with non-existent path (should not crash)
        test_path = Path("./test_data_folder")
        loader = DataLoader(test_path)
        logger.info("✓ DataLoader initialized successfully")

        # Test methods exist
        assert hasattr(loader, "load_all_data"), "load_all_data method missing"
        assert hasattr(loader, "get_inject_time"), "get_inject_time method missing"
        assert hasattr(loader, "extract_calling_patterns"), (
            "extract_calling_patterns method missing"
        )
        logger.info("✓ DataLoader has required methods")

        return True

    except Exception as e:
        logger.error(f"DataLoader test failed: {e}")
        return False


def test_adapter_init():
    """Test if MicroDigAdapter can be initialized"""
    logger.info("Testing MicroDigAdapter initialization...")

    try:
        from microdig import MicroDigAdapter

        adapter = MicroDigAdapter()
        logger.info("✓ MicroDigAdapter initialized successfully")

        # Test methods exist
        assert hasattr(adapter, "run_microdig_analysis"), (
            "run_microdig_analysis method missing"
        )
        logger.info("✓ MicroDigAdapter has required methods")

        return True

    except Exception as e:
        logger.error(f"MicroDigAdapter test failed: {e}")
        return False


def test_platform_interface():
    """Test if MicroDig platform interface can be initialized"""
    logger.info("Testing MicroDig platform interface...")

    try:
        from microdig import MicroDig

        microdig_alg = MicroDig()
        logger.info("✓ MicroDig platform class initialized successfully")

        # Test required methods exist
        assert hasattr(microdig_alg, "needs_cpu_count"), (
            "needs_cpu_count method missing"
        )
        cpu_count = microdig_alg.needs_cpu_count()
        logger.info(f"✓ CPU count requirement: {cpu_count}")

        return True

    except Exception as e:
        logger.error(f"Platform interface test failed: {e}")
        return False


def test_function_interface():
    """Test if the direct function interface works"""
    logger.info("Testing microdig_analysis function...")

    try:
        from microdig import microdig_analysis

        # Test that function exists and is callable
        assert callable(microdig_analysis), "microdig_analysis is not callable"
        logger.info("✓ microdig_analysis function is callable")

        # Test with invalid input (should return error gracefully)
        result = microdig_analysis(
            input_folder=Path("./non_existent_folder"),
            alarm_item="test-service",
            root_cause="test-service",
        )

        # Should return a dict with error information
        assert isinstance(result, dict), "Function should return a dictionary"
        logger.info("✓ microdig_analysis handles invalid input gracefully")

        return True

    except Exception as e:
        logger.error(f"Function interface test failed: {e}")
        return False


def test_cli_interface():
    """Test if CLI interface is available"""
    logger.info("Testing CLI interface...")

    try:
        from microdig import cli_app

        # Check if it's a Typer app or similar
        assert hasattr(cli_app, "callback") or hasattr(cli_app, "command"), (
            "CLI app structure not recognized"
        )
        logger.info("✓ CLI app is available")

        return True

    except Exception as e:
        logger.error(f"CLI interface test failed: {e}")
        return False


def test_package_structure():
    """Test the overall package structure"""
    logger.info("Testing package structure...")

    try:
        import microdig

        # Check if main components are accessible
        components = [
            "DataLoader",
            "MicroDigAdapter",
            "microdig_analysis",
            "MicroDig",
            "cli_app",
        ]

        for component in components:
            assert hasattr(microdig, component), (
                f"Component {component} not accessible from package"
            )
            logger.info(f"✓ {component} accessible from main package")

        return True

    except Exception as e:
        logger.error(f"Package structure test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and return summary"""
    logger.info("Starting MicroDig package tests...")
    logger.info("=" * 50)

    tests = [
        ("Import Test", test_imports),
        ("Data Loader Test", test_data_loader_init),
        ("Adapter Test", test_adapter_init),
        ("Platform Interface Test", test_platform_interface),
        ("Function Interface Test", test_function_interface),
        ("CLI Interface Test", test_cli_interface),
        ("Package Structure Test", test_package_structure),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                logger.info(f"✓ {test_name} PASSED")
            else:
                failed += 1
                logger.error(f"✗ {test_name} FAILED")
        except Exception as e:
            failed += 1
            logger.error(f"✗ {test_name} FAILED with exception: {e}")

    logger.info("\n" + "=" * 50)
    logger.info("TEST SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total tests: {len(tests)}")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")

    if failed == 0:
        logger.info("🎉 All tests passed! MicroDig package is ready.")
        return True
    else:
        logger.error(f"❌ {failed} test(s) failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
