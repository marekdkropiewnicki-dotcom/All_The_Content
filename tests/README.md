# Test Suite for All The Content Modpack

This directory contains comprehensive tests for validating the modpack configuration, documentation, and overall integrity.

## Overview

Since this is a modpack repository (not source code), the tests focus on:
- Manifest validation
- Configuration file integrity
- Documentation consistency
- Modpack structure and dependencies

## Test Files

- **test_manifest.py**: Validates `manifest.json` format, required fields, dependency format, and version consistency
- **test_config.py**: Validates configuration files in the `config/` directory
- **test_documentation.py**: Validates README.md and CHANGELOG.md structure and consistency
- **test_integration.py**: Integration tests for overall modpack integrity

## Running Tests

### Run all tests:
```bash
python -m unittest discover tests
```

### Run specific test file:
```bash
python -m unittest tests.test_manifest
python -m unittest tests.test_config
python -m unittest tests.test_documentation
python -m unittest tests.test_integration
```

### Run specific test class:
```bash
python -m unittest tests.test_manifest.TestManifest
```

### Run specific test method:
```bash
python -m unittest tests.test_manifest.TestManifest.test_version_number_format
```

### Run with verbose output:
```bash
python -m unittest discover tests -v
```

## Requirements

The test suite uses Python's built-in `unittest` framework and requires no external dependencies.

- Python 3.6 or higher

## Test Coverage Areas

### 1. Manifest Tests
- ✅ Valid JSON format
- ✅ Required fields present (name, version_number, website_url, description, dependencies)
- ✅ Semantic versioning format (X.Y.Z)
- ✅ Valid URL format
- ✅ Dependency format validation (Author-ModName-Version)
- ✅ No duplicate dependencies
- ✅ BepInEx dependency present
- ✅ Version consistency across files

### 2. Configuration Tests
- ✅ Config directory exists
- ✅ Config files are readable
- ✅ UTF-8 encoding
- ✅ BepInEx.cfg exists (core config)
- ✅ Proper file naming conventions
- ✅ No excessive trailing whitespace
- ✅ Config structure validation

### 3. Documentation Tests
- ✅ README.md exists and not empty
- ✅ Has proper title and sections
- ✅ Valid markdown link format
- ✅ Thunderstore reference present
- ✅ CHANGELOG.md exists
- ✅ Versions documented in descending order
- ✅ Latest version in changelog
- ✅ Consistent GitHub URLs

### 4. Integration Tests
- ✅ Icon.png exists and valid
- ✅ All required Thunderstore files present
- ✅ No sensitive files committed
- ✅ Valid repository structure
- ✅ Reasonable dependency count
- ✅ Core dependencies present
- ✅ Semantic versioning for all dependencies

## Continuous Integration

Tests can be integrated into CI/CD pipelines using the provided GitHub Actions workflow (`.github/workflows/test.yml`).

## Contributing

When adding new features or modifying the modpack:

1. Ensure all existing tests pass
2. Add new tests for new validation rules
3. Run tests locally before committing
4. Update this README if adding new test categories

## Test Philosophy

These tests serve as:
- **Quality gates**: Catch configuration errors before release
- **Documentation**: Demonstrate modpack requirements
- **Regression prevention**: Ensure consistency across updates

## Common Test Failures and Solutions

### "manifest.json must exist"
- Ensure you're running tests from the repository root
- Check that manifest.json is present

### "Version must follow semantic versioning"
- Update version to X.Y.Z format (e.g., 1.4.2)
- Ensure no letters or extra segments

### "BepInEx dependency must be present"
- Add BepInEx-BepInExPack dependency to manifest.json

### "UTF-8 encoding error"
- Convert config files to UTF-8 encoding
- Avoid special characters that aren't UTF-8 compatible

## Future Enhancements

Potential additions to the test suite:
- [ ] Automated dependency version checking against Thunderstore API
- [ ] Config file schema validation
- [ ] Markdown linting for documentation
- [ ] Performance tests for large dependency lists
- [ ] Compatibility matrix testing
