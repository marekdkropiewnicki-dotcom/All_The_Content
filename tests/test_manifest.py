"""
Test suite for manifest.json validation.

This module tests the Thunderstore manifest file to ensure it follows
the required format and contains valid data for modpack distribution.
"""

import unittest
import json
import os
import re
from pathlib import Path


class TestManifestStructure(unittest.TestCase):
    """Test the basic structure and required fields of manifest.json"""

    @classmethod
    def setUpClass(cls):
        """Load manifest.json once for all tests"""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"

        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_manifest_exists(self):
        """Test that manifest.json exists"""
        self.assertTrue(
            self.manifest_path.exists(),
            "manifest.json file must exist in repository root"
        )

    def test_manifest_is_valid_json(self):
        """Test that manifest.json is valid JSON"""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"manifest.json is not valid JSON: {e}")

    def test_required_fields_present(self):
        """Test that all required Thunderstore fields are present"""
        required_fields = ['name', 'version_number', 'website_url', 'description', 'dependencies']

        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.manifest,
                    f"Required field '{field}' is missing from manifest.json"
                )

    def test_name_field(self):
        """Test that the name field is valid"""
        self.assertIsInstance(self.manifest['name'], str, "name must be a string")
        self.assertGreater(len(self.manifest['name']), 0, "name must not be empty")
        self.assertLessEqual(
            len(self.manifest['name']),
            100,
            "name should be 100 characters or less"
        )

    def test_version_number_format(self):
        """Test that version_number follows semantic versioning (X.Y.Z)"""
        version = self.manifest['version_number']
        self.assertIsInstance(version, str, "version_number must be a string")

        # Semantic versioning pattern: X.Y.Z where X, Y, Z are integers
        semver_pattern = r'^\d+\.\d+\.\d+$'
        self.assertRegex(
            version,
            semver_pattern,
            f"version_number '{version}' must follow semantic versioning (X.Y.Z)"
        )

    def test_website_url_field(self):
        """Test that website_url is a valid URL"""
        url = self.manifest['website_url']
        self.assertIsInstance(url, str, "website_url must be a string")

        # Basic URL validation
        url_pattern = r'^https?://.+'
        self.assertRegex(
            url,
            url_pattern,
            "website_url must be a valid HTTP/HTTPS URL"
        )

    def test_description_field(self):
        """Test that description is present and reasonable"""
        description = self.manifest['description']
        self.assertIsInstance(description, str, "description must be a string")
        self.assertGreater(
            len(description),
            10,
            "description should be at least 10 characters"
        )
        self.assertLessEqual(
            len(description),
            250,
            "description should be 250 characters or less for Thunderstore"
        )

    def test_dependencies_is_list(self):
        """Test that dependencies field is a list"""
        self.assertIsInstance(
            self.manifest['dependencies'],
            list,
            "dependencies must be a list"
        )

    def test_dependencies_not_empty(self):
        """Test that dependencies list is not empty"""
        self.assertGreater(
            len(self.manifest['dependencies']),
            0,
            "dependencies list should not be empty (at minimum BepInEx is required)"
        )


class TestManifestDependencies(unittest.TestCase):
    """Test the dependencies array in manifest.json"""

    @classmethod
    def setUpClass(cls):
        """Load manifest.json once for all tests"""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"

        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_dependency_format(self):
        """Test that each dependency follows the Author-ModName-Version format"""
        dependency_pattern = r'^[\w\d_]+-[\w\d_]+-\d+\.\d+\.\d+$'

        for dep in self.manifest['dependencies']:
            with self.subTest(dependency=dep):
                self.assertIsInstance(dep, str, f"Dependency '{dep}' must be a string")
                self.assertRegex(
                    dep,
                    dependency_pattern,
                    f"Dependency '{dep}' must follow format: Author-ModName-Version"
                )

    def test_bepinex_dependency_present(self):
        """Test that BepInEx is listed as a dependency"""
        bepinex_deps = [dep for dep in self.manifest['dependencies'] if 'BepInEx' in dep]
        self.assertGreater(
            len(bepinex_deps),
            0,
            "BepInEx must be listed as a dependency for Content Warning modpacks"
        )

    def test_no_duplicate_dependencies(self):
        """Test that there are no duplicate dependencies"""
        deps = self.manifest['dependencies']
        unique_deps = set(deps)

        if len(deps) != len(unique_deps):
            duplicates = [dep for dep in deps if deps.count(dep) > 1]
            self.fail(f"Duplicate dependencies found: {set(duplicates)}")

    def test_dependency_versions_valid(self):
        """Test that all dependency versions are valid semantic versions"""
        for dep in self.manifest['dependencies']:
            with self.subTest(dependency=dep):
                parts = dep.split('-')
                self.assertGreaterEqual(
                    len(parts),
                    3,
                    f"Dependency '{dep}' must have at least 3 parts (Author-ModName-Version)"
                )

                version = parts[-1]
                version_pattern = r'^\d+\.\d+\.\d+$'
                self.assertRegex(
                    version,
                    version_pattern,
                    f"Version '{version}' in dependency '{dep}' must be semantic (X.Y.Z)"
                )


class TestManifestConsistency(unittest.TestCase):
    """Test consistency between manifest.json and other repository files"""

    @classmethod
    def setUpClass(cls):
        """Load manifest.json and other files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"
        cls.readme_path = cls.repo_root / "README.md"
        cls.changelog_path = cls.repo_root / "CHANGELOG.md"

        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_readme_exists(self):
        """Test that README.md exists"""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md should exist in repository"
        )

    def test_changelog_exists(self):
        """Test that CHANGELOG.md exists"""
        self.assertTrue(
            self.changelog_path.exists(),
            "CHANGELOG.md should exist in repository"
        )

    def test_version_in_changelog(self):
        """Test that current version is documented in CHANGELOG.md"""
        if not self.changelog_path.exists():
            self.skipTest("CHANGELOG.md does not exist")

        with open(self.changelog_path, 'r', encoding='utf-8') as f:
            changelog_content = f.read()

        version = self.manifest['version_number']
        self.assertIn(
            version,
            changelog_content,
            f"Version {version} should be documented in CHANGELOG.md"
        )

    def test_name_consistency(self):
        """Test that modpack name is consistent across files"""
        if not self.readme_path.exists():
            self.skipTest("README.md does not exist")

        with open(self.readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        name = self.manifest['name']
        # Allow for variations like "All The Content" vs "All_The_Content"
        name_normalized = name.replace('_', ' ')

        self.assertTrue(
            name in readme_content or name_normalized in readme_content,
            f"Modpack name '{name}' should appear in README.md"
        )

    def test_icon_exists(self):
        """Test that icon.png exists"""
        icon_path = self.repo_root / "icon.png"
        self.assertTrue(
            icon_path.exists(),
            "icon.png should exist for Thunderstore package"
        )

    def test_icon_size(self):
        """Test that icon.png is a reasonable size"""
        icon_path = self.repo_root / "icon.png"
        if not icon_path.exists():
            self.skipTest("icon.png does not exist")

        file_size = icon_path.stat().st_size
        # Thunderstore recommends 256x256 PNG, typically under 500KB
        self.assertLess(
            file_size,
            1024 * 1024,  # 1MB
            "icon.png should be under 1MB for optimal package size"
        )


if __name__ == '__main__':
    unittest.main()
