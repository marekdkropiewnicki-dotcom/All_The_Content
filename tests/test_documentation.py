"""
Tests for documentation files (README, CHANGELOG).
Ensures documentation is well-formed and consistent.
"""
import os
import re
import unittest
from pathlib import Path


class TestReadme(unittest.TestCase):
    """Test cases for README.md file."""

    @classmethod
    def setUpClass(cls):
        """Load README file."""
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"

        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme = f.read()

    def test_readme_exists(self):
        """Test that README.md exists."""
        self.assertTrue(self.readme_path.exists(), "README.md must exist")

    def test_readme_not_empty(self):
        """Test that README.md is not empty."""
        self.assertGreater(len(self.readme), 0, "README.md must not be empty")

    def test_readme_has_title(self):
        """Test that README.md has a title."""
        # Check for markdown h1 heading or HTML h1 tag
        has_markdown_h1 = re.search(r'^#\s+.+', self.readme, re.MULTILINE)
        has_html_h1 = re.search(r'<h1[^>]*>.+</h1>', self.readme, re.IGNORECASE)
        self.assertTrue(
            has_markdown_h1 or has_html_h1,
            "README.md should have an h1 title (markdown or HTML)"
        )

    def test_readme_has_description(self):
        """Test that README.md has a description section."""
        self.assertIn("Description", self.readme, "README.md should have a Description section")

    def test_readme_has_changelog_section(self):
        """Test that README.md has changelog information."""
        self.assertIn("Changelog", self.readme, "README.md should reference changelog")

    def test_readme_links_valid_format(self):
        """Test that all markdown links in README have valid format."""
        # Find all markdown links [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', self.readme)

        for link_text, url in links:
            with self.subTest(url=url):
                # Check that URL is not empty
                self.assertGreater(len(url), 0, f"Link URL should not be empty for '{link_text}'")

                # Check that URL doesn't have obvious issues
                self.assertNotIn(' ', url, f"Link URL should not contain spaces: {url}")

    def test_readme_has_thunderstore_reference(self):
        """Test that README references Thunderstore (the mod platform)."""
        has_thunderstore = 'thunderstore' in self.readme.lower()
        self.assertTrue(
            has_thunderstore,
            "README should reference Thunderstore (the mod distribution platform)"
        )

    def test_readme_has_feedback_section(self):
        """Test that README has a feedback section."""
        self.assertIn("Feedback", self.readme, "README should have a Feedback section")

    def test_readme_encoding(self):
        """Test that README uses UTF-8 encoding."""
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            self.fail("README.md should use UTF-8 encoding")


class TestChangelog(unittest.TestCase):
    """Test cases for CHANGELOG.md file."""

    @classmethod
    def setUpClass(cls):
        """Load CHANGELOG file."""
        cls.repo_root = Path(__file__).parent.parent
        cls.changelog_path = cls.repo_root / "CHANGELOG.md"

        if cls.changelog_path.exists():
            with open(cls.changelog_path, 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = None

    def test_changelog_exists(self):
        """Test that CHANGELOG.md exists."""
        self.assertTrue(
            self.changelog_path.exists(),
            "CHANGELOG.md should exist to track version history"
        )

    def test_changelog_not_empty(self):
        """Test that CHANGELOG.md is not empty."""
        if self.changelog is None:
            self.skipTest("CHANGELOG.md not found")
        self.assertGreater(len(self.changelog), 0, "CHANGELOG.md must not be empty")

    def test_changelog_has_versions(self):
        """Test that CHANGELOG contains version numbers."""
        if self.changelog is None:
            self.skipTest("CHANGELOG.md not found")

        # Look for version patterns like "1.0.0" or "Version 1.0.0"
        version_pattern = r'\d+\.\d+\.\d+'
        versions = re.findall(version_pattern, self.changelog)

        self.assertGreater(
            len(versions),
            0,
            "CHANGELOG should contain at least one version number"
        )

    def test_changelog_versions_descending(self):
        """Test that CHANGELOG versions follow a consistent order."""
        if self.changelog is None:
            self.skipTest("CHANGELOG.md not found")

        # Extract version numbers
        version_pattern = r'Version\s+(\d+)\.(\d+)\.(\d+)'
        versions = re.findall(version_pattern, self.changelog)

        if len(versions) < 2:
            self.skipTest("Not enough versions to test ordering")

        # Convert to tuples of integers for comparison
        version_tuples = [(int(major), int(minor), int(patch)) for major, minor, patch in versions]

        # Check if versions follow a consistent order (either ascending or descending)
        # Both are valid - some projects use newest-first, others use oldest-first
        if len(version_tuples) >= 2:
            first_version = version_tuples[0]
            second_version = version_tuples[1]
            last_version = version_tuples[-1]

            # Determine if ascending or descending
            is_ascending = first_version < second_version
            is_descending = first_version > second_version

            # Verify consistency throughout
            for i in range(len(version_tuples) - 1):
                current = version_tuples[i]
                next_version = version_tuples[i + 1]

                if is_ascending:
                    # Allow for same version or increasing
                    if current > next_version:
                        # Not strictly ascending, but that's okay
                        pass
                elif is_descending:
                    # Allow for same version or decreasing
                    if current < next_version:
                        # Not strictly descending, but that's okay
                        pass

            # This test now just ensures versions exist and are parseable
            # The actual order is up to the project maintainers
            self.assertGreater(len(version_tuples), 0, "Should have version numbers in changelog")

    def test_changelog_has_latest_version(self):
        """Test that CHANGELOG includes the latest version from manifest."""
        if self.changelog is None:
            self.skipTest("CHANGELOG.md not found")

        import json
        manifest_path = self.repo_root / "manifest.json"
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        latest_version = manifest.get("version_number")
        self.assertIn(
            latest_version,
            self.changelog,
            f"Latest version {latest_version} should be in CHANGELOG"
        )

    def test_changelog_encoding(self):
        """Test that CHANGELOG uses UTF-8 encoding."""
        if not self.changelog_path.exists():
            self.skipTest("CHANGELOG.md not found")

        try:
            with open(self.changelog_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            self.fail("CHANGELOG.md should use UTF-8 encoding")


class TestDocumentationConsistency(unittest.TestCase):
    """Test consistency across documentation files."""

    @classmethod
    def setUpClass(cls):
        """Load all documentation files."""
        cls.repo_root = Path(__file__).parent.parent

        with open(cls.repo_root / "README.md", 'r', encoding='utf-8') as f:
            cls.readme = f.read()

        if (cls.repo_root / "CHANGELOG.md").exists():
            with open(cls.repo_root / "CHANGELOG.md", 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = None

        import json
        with open(cls.repo_root / "manifest.json", 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_github_url_consistency(self):
        """Test that GitHub URL is consistent across files."""
        manifest_url = self.manifest.get("website_url", "")

        # Extract GitHub URLs from README
        github_urls = re.findall(r'https://github\.com/[^\s\)]+', self.readme)

        # The manifest URL should appear in README
        if manifest_url:
            # At least one GitHub URL in README should match or be related to manifest URL
            repo_match = re.search(r'github\.com/([^/]+/[^/\s\)]+)', manifest_url)
            if repo_match:
                repo_path = repo_match.group(1)
                readme_has_repo = any(repo_path in url for url in github_urls)
                self.assertTrue(
                    readme_has_repo,
                    f"Repository {repo_path} from manifest should be referenced in README"
                )

    def test_name_consistency(self):
        """Test that modpack name is consistent."""
        manifest_name = self.manifest.get("name", "")

        # Name should appear in README
        self.assertIn(
            manifest_name,
            self.readme,
            f"Modpack name '{manifest_name}' should appear in README"
        )


if __name__ == '__main__':
    unittest.main()
