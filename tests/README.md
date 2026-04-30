# Test Suite Documentation

This directory contains comprehensive tests for the **All The Content** modpack to ensure quality, consistency, and compliance with Thunderstore requirements.

## Overview

The test suite validates:
- **Manifest structure** - Ensures manifest.json follows Thunderstore format
- **Configuration files** - Validates all .cfg files in the config directory
- **Documentation** - Checks README.md and CHANGELOG.md for completeness
- **Integration** - Tests consistency between different components

## Test Files

### test_manifest.py
Tests for manifest.json validation:
- Required fields presence (name, version_number, website_url, description, dependencies)
- Semantic versioning format (X.Y.Z)
- Valid dependency format (Author-ModName-Version)
- BepInEx dependency requirement
- No duplicate dependencies
- Consistency with other files

**Test Count:** 13 tests across 3 test classes

### test_config.py
Tests for configuration file validation:
- Config directory exists with .cfg files
- All config files are readable
- Basic INI format validation (where applicable)
- No invalid control characters
- BepInEx.cfg presence and structure
- Config naming conventions

**Test Count:** 7 tests across 5 test classes

### test_documentation.py
Tests for documentation validation:
- README.md existence and structure
- Title and description presence
- Proper markdown formatting
- Links and references
- CHANGELOG.md structure
- Version history completeness
- Current version documentation
- No placeholder text
- Required files for Thunderstore package

**Test Count:** 11 tests across 4 test classes

### test_integration.py
Integration tests:
- Manifest and config consistency
- BepInEx dependency/config alignment
- Version consistency across files
- Website URL consistency
- Description consistency
- No sensitive files in repository
- No circular dependencies
- Critical dependencies present

**Test Count:** 7 tests across 4 test classes

## Running Tests

### Quick Start

Run all tests using the provided script:

```bash
./run_tests.sh
```

### Manual Execution

Run all tests:
```bash
python3 -m unittest discover tests -v
```

Run specific test file:
```bash
python3 -m unittest tests.test_manifest -v
```

Run specific test class:
```bash
python3 -m unittest tests.test_manifest.TestManifestStructure -v
```

Run specific test:
```bash
python3 -m unittest tests.test_manifest.TestManifestStructure.test_version_number_format -v
```

### Requirements

- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

## Test Coverage Summary

**Total Tests:** 38 tests across 16 test classes

### Coverage by Area:
- **Manifest Validation:** 13 tests
- **Configuration Validation:** 7 tests
- **Documentation Validation:** 11 tests
- **Integration Testing:** 7 tests

### What's Tested:

✅ Manifest.json structure and format
✅ Semantic versioning compliance
✅ Dependency format and validity
✅ BepInEx requirement
✅ Configuration file readability
✅ Config file format validation
✅ README.md completeness
✅ CHANGELOG.md structure
✅ Version consistency
✅ Documentation quality
✅ Cross-file consistency
✅ Package integrity
✅ No sensitive files
✅ Critical dependencies

## Continuous Integration

Tests automatically run on:
- Every push to main/master/develop branches
- Every pull request
- Python versions: 3.8, 3.9, 3.10, 3.11

See `.github/workflows/test.yml` for CI configuration.

## Adding New Tests

To add new tests:

1. Create a new test class in the appropriate test file
2. Inherit from `unittest.TestCase`
3. Name test methods starting with `test_`
4. Use descriptive names and docstrings
5. Include subtests for testing multiple items

Example:
```python
class TestNewFeature(unittest.TestCase):
    """Test description"""

    def test_something(self):
        """Test that something works"""
        self.assertTrue(condition, "Error message")
```

## Test Philosophy

These tests follow these principles:

- **Comprehensive:** Cover all critical aspects of the modpack
- **Maintainable:** Easy to understand and modify
- **Fast:** Execute quickly for rapid feedback
- **Independent:** Tests don't depend on each other
- **Informative:** Clear error messages when tests fail

## Common Issues

### Test Failures

If tests fail:

1. Read the error message carefully
2. Check the specific file/line mentioned
3. Verify the file format matches requirements
4. Ensure all required files exist
5. Check version numbers are semantic (X.Y.Z)

### Python Not Found

Ensure Python 3.8+ is installed:
```bash
python3 --version
```

### Permission Denied

Make the test script executable:
```bash
chmod +x run_tests.sh
```

## Contributing

When contributing to the modpack:

1. Run tests locally before committing
2. Ensure all tests pass
3. Add new tests for new features
4. Update this README if test structure changes

## Support

For issues or questions:
- Check existing test output for specific errors
- Review Thunderstore documentation
- Visit the Content Warning Modding Discord

---

**Last Updated:** 2026-04-30
**Test Suite Version:** 1.0.0
