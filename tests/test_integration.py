"""
Integration tests for the modpack.
Tests overall consistency and integrity of the modpack.
"""
import json
import os
import re
import unittest
from pathlib import Path


class TestModpackIntegrity(unittest.TestCase):
    """Test overall modpack integrity."""

    @classmethod
    def setUpClass(cls):
        """Load all necessary files."""
        cls.repo_root = Path(__file__).parent.parent

        with open(cls.repo_root / "manifest.json", 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

        cls.config_dir = cls.repo_root / "config"
        cls.config_files = list(cls.config_dir.glob("*.cfg")) if cls.config_dir.exists() else []

    def test_icon_exists(self):
        """Test that icon.png exists."""
        icon_path = self.repo_root / "icon.png"
        self.assertTrue(icon_path.exists(), "icon.png must exist for Thunderstore")

    def test_icon_valid(self):
        """Test that icon.png is a valid image file."""
        icon_path = self.repo_root / "icon.png"
        if icon_path.exists():
            # Check file size is reasonable (not empty, not too large)
            size = icon_path.stat().st_size
            self.assertGreater(size, 100, "Icon file should not be empty")
            self.assertLess(size, 10 * 1024 * 1024, "Icon should be less than 10MB")

    def test_required_files_present(self):
        """Test that all required files for Thunderstore are present."""
        required_files = ["manifest.json", "README.md", "icon.png"]

        for filename in required_files:
            with self.subTest(file=filename):
                file_path = self.repo_root / filename
                self.assertTrue(
                    file_path.exists(),
                    f"{filename} is required for Thunderstore modpack"
                )

    def test_no_sensitive_files(self):
        """Test that no sensitive files are committed."""
        sensitive_patterns = [
            "*.key", "*.pem", "*.pfx", "*.p12",
            "*password*", "*secret*", "*.env"
        ]

        for pattern in sensitive_patterns:
            files = list(self.repo_root.glob(pattern))
            # Filter out test files
            files = [f for f in files if 'test' not in str(f).lower()]
            self.assertEqual(
                len(files),
                0,
                f"Sensitive files matching '{pattern}' should not be committed"
            )

    def test_file_structure_valid(self):
        """Test that the repository has a valid file structure."""
        # Expected directories/files
        self.assertTrue((self.repo_root / "config").exists(), "config directory should exist")
        self.assertTrue(
            (self.repo_root / "config").is_dir(),
            "config should be a directory"
        )

    def test_dependency_count_reasonable(self):
        """Test that dependency count is reasonable."""
        dependencies = self.manifest.get("dependencies", [])

        # Should have at least BepInEx
        self.assertGreater(
            len(dependencies),
            0,
            "Should have at least one dependency (BepInEx)"
        )

        # Warn if too many dependencies (might cause performance issues)
        # This is a soft limit - modpacks can have many dependencies
        if len(dependencies) > 100:
            # This is just a warning, not a failure
            pass

    def test_git_directory_structure(self):
        """Test that git repository is properly structured."""
        git_dir = self.repo_root / ".git"
        self.assertTrue(git_dir.exists(), "Should be a git repository")


class TestVersionConsistency(unittest.TestCase):
    """Test version consistency across the project."""

    @classmethod
    def setUpClass(cls):
        """Load necessary files."""
        cls.repo_root = Path(__file__).parent.parent

        with open(cls.repo_root / "manifest.json", 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

        if (cls.repo_root / "CHANGELOG.md").exists():
            with open(cls.repo_root / "CHANGELOG.md", 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = None

    def test_version_format_valid(self):
        """Test that version follows semantic versioning."""
        version = self.manifest.get("version_number")
        parts = version.split('.')

        self.assertEqual(len(parts), 3, "Version should have 3 parts (major.minor.patch)")

        for part in parts:
            self.assertTrue(
                part.isdigit(),
                f"Version part '{part}' should be numeric"
            )

    def test_version_in_changelog(self):
        """Test that current version is documented in changelog."""
        if self.changelog is None:
            self.skipTest("CHANGELOG.md not found")

        version = self.manifest.get("version_number")
        self.assertIn(
            version,
            self.changelog,
            f"Version {version} should be documented in CHANGELOG"
        )


class TestDependencyIntegrity(unittest.TestCase):
    """Test dependency integrity and consistency."""

    @classmethod
    def setUpClass(cls):
        """Load manifest."""
        cls.repo_root = Path(__file__).parent.parent

        with open(cls.repo_root / "manifest.json", 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_dependencies_alphabetically_sorted(self):
        """Test if dependencies are sorted (good practice but not required)."""
        dependencies = self.manifest.get("dependencies", [])

        # This is a recommendation, not a strict requirement
        sorted_deps = sorted(dependencies)

        # We won't fail the test, but we can check
        if dependencies != sorted_deps:
            # Just a note - not failing the test
            pass

    def test_known_incompatibilities(self):
        """Test for known incompatible mod combinations."""
        dependencies = self.manifest.get("dependencies", [])
        dep_names = [dep.split('-')[1] if '-' in dep else dep for dep in dependencies]

        # Currently no known incompatibilities to test
        # This is a placeholder for future checks
        pass

    def test_core_dependencies_present(self):
        """Test that core/essential dependencies are present."""
        dependencies = self.manifest.get("dependencies", [])

        # BepInEx is essential
        has_bepinex = any("BepInEx" in dep for dep in dependencies)
        self.assertTrue(has_bepinex, "BepInEx is required for Content Warning mods")

    def test_dependency_versions_not_ancient(self):
        """Test that dependency versions follow reasonable patterns."""
        dependencies = self.manifest.get("dependencies", [])

        for dep in dependencies:
            with self.subTest(dependency=dep):
                parts = dep.rsplit('-', 1)
                if len(parts) == 2:
                    version = parts[1]
                    version_parts = version.split('.')

                    # Basic sanity check - version should have 3 parts
                    self.assertEqual(
                        len(version_parts),
                        3,
                        f"Dependency {dep} should have semantic version"
                    )


if __name__ == '__main__':
    unittest.main()
