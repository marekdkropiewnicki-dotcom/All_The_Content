# Test Suite Documentation

## Overview

This test suite provides comprehensive validation for the All The Content modpack. It ensures that the modpack structure, configuration, and documentation meet Thunderstore requirements and maintain quality standards.

## Test Coverage

### 1. Manifest Tests (`test_manifest.py`)

Validates the `manifest.json` file for Thunderstore compatibility:

- **Required fields**: Checks that all mandatory fields are present (name, version_number, website_url, description, dependencies)
- **Semantic versioning**: Ensures version numbers follow X.Y.Z format
- **Dependency format**: Validates that dependencies follow the `Author-ModName-Version` format
- **BepInEx requirement**: Verifies that BepInEx is included as a dependency
- **No duplicates**: Ensures no duplicate dependencies are listed
- **URL validation**: Checks that website URLs are properly formatted

**Test Count**: 12 tests

### 2. Configuration Tests (`test_config.py`)

Validates configuration files in the `config/` directory:

- **Directory structure**: Ensures config directory exists and contains .cfg files
- **File readability**: Verifies all config files can be opened and read
- **UTF-8 encoding**: Ensures proper text encoding
- **BepInEx config**: Checks that BepInEx.cfg exists and is properly configured
- **Consistency**: Validates that configs match dependencies in manifest

**Test Count**: 7 tests

### 3. Documentation Tests (`test_documentation.py`)

Validates README.md and CHANGELOG.md:

- **File existence**: Ensures documentation files exist
- **Content validation**: Checks that files are not empty and contain required sections
- **Version tracking**: Verifies current version is documented in CHANGELOG
- **Link validation**: Ensures markdown links are properly formatted
- **Consistency**: Validates that information matches across manifest and documentation

**Test Count**: 11 tests

### 4. Integration Tests (`test_integration.py`)

Validates overall modpack structure and integrity:

- **Required files**: Checks for manifest.json, README.md, and icon.png
- **Icon validation**: Verifies icon.png is a valid PNG file with reasonable size
- **Security checks**: Ensures no sensitive files are accidentally included
- **Package size**: Validates total modpack size is reasonable for distribution
- **Dependency integrity**: Checks for duplicate mods and reasonable dependency count

**Test Count**: 6 tests

## Running Tests

### Local Testing

Run all tests using the provided script:

```bash
./run_tests.sh
```

Or run tests directly with Python:

```bash
python3 -m unittest discover tests -v
```

### Run Specific Test Files

```bash
python3 -m unittest tests.test_manifest -v
python3 -m unittest tests.test_config -v
python3 -m unittest tests.test_documentation -v
python3 -m unittest tests.test_integration -v
```

### Run Individual Tests

```bash
python3 -m unittest tests.test_manifest.TestManifest.test_version_number_format -v
```

## Continuous Integration

Tests are automatically run via GitHub Actions on:
- Push to main, master, or develop branches
- Pull requests targeting these branches

The CI pipeline tests against Python versions 3.8, 3.9, 3.10, and 3.11.

## Test Requirements

- Python 3.8 or higher
- Standard library only (no external dependencies required)

## Adding New Tests

When adding new tests:

1. Create tests in the appropriate test file or add a new file in `tests/`
2. Follow the existing naming convention: `test_*.py`
3. Use `unittest.TestCase` as the base class
4. Add descriptive docstrings to test methods
5. Use `self.subTest()` for testing multiple items in a loop
6. Run tests locally before committing

## Test Success Criteria

All tests must pass before:
- Merging pull requests
- Creating new releases
- Publishing to Thunderstore

## Common Test Failures

### Manifest Validation Failures
- **Invalid version format**: Ensure version follows X.Y.Z format (e.g., 1.4.2)
- **Dependency format**: Dependencies must be `Author-ModName-Version`
- **Missing BepInEx**: BepInEx must be listed in dependencies

### Config File Failures
- **Missing files**: Ensure all .cfg files are present in the config/ directory
- **Encoding issues**: Use UTF-8 encoding for all config files

### Documentation Failures
- **Outdated version**: Update CHANGELOG.md when version changes
- **Broken links**: Check that all URLs in README.md are valid

### Integration Failures
- **Large package size**: Optimize or remove large files
- **Duplicate dependencies**: Remove duplicate mods with different versions

## Maintenance

Update tests when:
- Thunderstore requirements change
- New validation rules are needed
- Community standards evolve
- New modpack features are added

## Contact

For issues or questions about the test suite, please report them on the [GitHub repository](https://github.com/PEPOAFONSO/All_The_Content).
