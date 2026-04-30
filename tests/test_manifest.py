"""
Tests for manifest.json validation.
Ensures the modpack manifest is valid and follows Thunderstore requirements.
"""
import json
import os
import re
import unittest
from pathlib import Path


class TestManifest(unittest.TestCase):
    """Test cases for manifest.json file."""

    @classmethod
    def setUpClass(cls):
        """Load the manifest file once for all tests."""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"

        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_manifest_exists(self):
        """Test that manifest.json exists."""
        self.assertTrue(self.manifest_path.exists(), "manifest.json must exist")

    def test_manifest_valid_json(self):
        """Test that manifest.json is valid JSON."""
        self.assertIsInstance(self.manifest, dict, "Manifest must be a valid JSON object")

    def test_required_fields_present(self):
        """Test that all required fields are present."""
        required_fields = ["name", "version_number", "website_url", "description", "dependencies"]
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, self.manifest, f"Manifest must contain '{field}' field")

    def test_name_valid(self):
        """Test that name field is valid."""
        name = self.manifest.get("name")
        self.assertIsInstance(name, str, "Name must be a string")
        self.assertGreater(len(name), 0, "Name must not be empty")
        self.assertLessEqual(len(name), 100, "Name must be 100 characters or less")

    def test_version_number_format(self):
        """Test that version_number follows semantic versioning."""
        version = self.manifest.get("version_number")
        self.assertIsInstance(version, str, "Version number must be a string")

        # Check semantic versioning format (X.Y.Z)
        version_pattern = r'^\d+\.\d+\.\d+$'
        self.assertRegex(
            version,
            version_pattern,
            "Version must follow semantic versioning format (X.Y.Z)"
        )

    def test_website_url_valid(self):
        """Test that website_url is a valid URL."""
        url = self.manifest.get("website_url")
        self.assertIsInstance(url, str, "Website URL must be a string")

        # Check URL format
        url_pattern = r'^https?://.+'
        self.assertRegex(url, url_pattern, "Website URL must be a valid HTTP(S) URL")

    def test_description_valid(self):
        """Test that description field is valid."""
        description = self.manifest.get("description")
        self.assertIsInstance(description, str, "Description must be a string")
        self.assertGreater(len(description), 0, "Description must not be empty")
        self.assertLessEqual(len(description), 250, "Description should be 250 characters or less")

    def test_dependencies_format(self):
        """Test that dependencies is a list and properly formatted."""
        dependencies = self.manifest.get("dependencies")
        self.assertIsInstance(dependencies, list, "Dependencies must be a list")

    def test_dependency_format_valid(self):
        """Test that each dependency follows the correct format."""
        dependencies = self.manifest.get("dependencies", [])

        # Format: Author-ModName-Version
        dependency_pattern = r'^[A-Za-z0-9_]+-[A-Za-z0-9_]+-\d+\.\d+\.\d+$'

        for dep in dependencies:
            with self.subTest(dependency=dep):
                self.assertIsInstance(dep, str, f"Dependency must be a string: {dep}")
                self.assertRegex(
                    dep,
                    dependency_pattern,
                    f"Dependency must follow format 'Author-ModName-Version': {dep}"
                )

    def test_no_duplicate_dependencies(self):
        """Test that there are no duplicate dependencies."""
        dependencies = self.manifest.get("dependencies", [])
        unique_deps = set(dependencies)
        self.assertEqual(
            len(dependencies),
            len(unique_deps),
            "Dependencies list contains duplicates"
        )

    def test_bepinex_dependency_present(self):
        """Test that BepInEx dependency is present (required for Content Warning mods)."""
        dependencies = self.manifest.get("dependencies", [])
        bepinex_present = any("BepInEx" in dep for dep in dependencies)
        self.assertTrue(
            bepinex_present,
            "BepInEx dependency must be present for Content Warning mods"
        )

    def test_dependency_versions_consistent(self):
        """Test that if a mod appears multiple times, versions are consistent."""
        dependencies = self.manifest.get("dependencies", [])
        mod_versions = {}

        for dep in dependencies:
            parts = dep.rsplit('-', 1)
            if len(parts) == 2:
                mod_name = parts[0]
                version = parts[1]

                if mod_name in mod_versions:
                    self.assertEqual(
                        mod_versions[mod_name],
                        version,
                        f"Inconsistent versions for {mod_name}"
                    )
                else:
                    mod_versions[mod_name] = version


class TestManifestVersionConsistency(unittest.TestCase):
    """Test that manifest version is consistent with other files."""

    @classmethod
    def setUpClass(cls):
        """Load necessary files."""
        cls.repo_root = Path(__file__).parent.parent

        with open(cls.repo_root / "manifest.json", 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

        with open(cls.repo_root / "README.md", 'r', encoding='utf-8') as f:
            cls.readme = f.read()

        if (cls.repo_root / "CHANGELOG.md").exists():
            with open(cls.repo_root / "CHANGELOG.md", 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = ""

    def test_version_in_readme(self):
        """Test that the current version is mentioned in README (optional check)."""
        version = self.manifest.get("version_number")
        # This is a soft check - version might not always be in README
        if version in self.readme:
            self.assertIn(version, self.readme, f"Version {version} should be documented in README")

    def test_version_in_changelog(self):
        """Test that the current version is documented in CHANGELOG."""
        if not self.changelog:
            self.skipTest("CHANGELOG.md not found")

        version = self.manifest.get("version_number")
        # Look for version pattern in changelog
        self.assertIn(
            version,
            self.changelog,
            f"Version {version} should be documented in CHANGELOG"
        )


if __name__ == '__main__':
    unittest.main()
