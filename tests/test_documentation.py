"""
Tests for documentation files (README, CHANGELOG)
"""
import json
import os
import re
import unittest


class TestDocumentation(unittest.TestCase):
    """Test suite for validating documentation files"""

    @classmethod
    def setUpClass(cls):
        """Load documentation files"""
        base_path = os.path.dirname(os.path.dirname(__file__))

        cls.readme_path = os.path.join(base_path, 'README.md')
        cls.changelog_path = os.path.join(base_path, 'CHANGELOG.md')

        if os.path.exists(cls.readme_path):
            with open(cls.readme_path, 'r', encoding='utf-8') as f:
                cls.readme = f.read()
        else:
            cls.readme = None

        if os.path.exists(cls.changelog_path):
            with open(cls.changelog_path, 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = None

        with open(os.path.join(base_path, 'manifest.json'), 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_readme_exists(self):
        """Test that README.md exists"""
        self.assertTrue(
            os.path.exists(self.readme_path),
            "README.md must exist"
        )

    def test_readme_not_empty(self):
        """Test that README.md is not empty"""
        if self.readme:
            self.assertGreater(
                len(self.readme),
                0,
                "README.md should not be empty"
            )

    def test_readme_has_title(self):
        """Test that README has a title"""
        if self.readme:
            # Check for markdown h1 header
            self.assertTrue(
                re.search(r'^#\s+.+', self.readme, re.MULTILINE) or
                re.search(r'^<h1>.+</h1>', self.readme, re.MULTILINE),
                "README should have a title (h1 header)"
            )

    def test_readme_has_description(self):
        """Test that README mentions the description"""
        if self.readme:
            # Should contain description or summary section
            self.assertTrue(
                'description' in self.readme.lower() or
                'about' in self.readme.lower(),
                "README should have a description or about section"
            )

    def test_changelog_exists(self):
        """Test that CHANGELOG.md exists"""
        self.assertTrue(
            os.path.exists(self.changelog_path),
            "CHANGELOG.md should exist"
        )

    def test_changelog_not_empty(self):
        """Test that CHANGELOG.md is not empty"""
        if self.changelog:
            self.assertGreater(
                len(self.changelog),
                0,
                "CHANGELOG.md should not be empty"
            )

    def test_changelog_has_current_version(self):
        """Test that CHANGELOG mentions the current version"""
        if self.changelog:
            current_version = self.manifest.get('version_number')
            self.assertIn(
                current_version,
                self.changelog,
                f"CHANGELOG should document current version {current_version}"
            )

    def test_changelog_version_format(self):
        """Test that CHANGELOG versions follow semantic versioning"""
        if self.changelog:
            # Find all version mentions
            version_pattern = r'\d+\.\d+\.\d+'
            versions = re.findall(version_pattern, self.changelog)

            self.assertGreater(
                len(versions),
                0,
                "CHANGELOG should contain version numbers"
            )

    def test_readme_links_valid(self):
        """Test that README contains valid markdown links"""
        if self.readme:
            # Find markdown links [text](url)
            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            links = re.findall(link_pattern, self.readme)

            for text, url in links:
                with self.subTest(link=url):
                    # Check that URL is not empty
                    self.assertTrue(
                        len(url) > 0,
                        f"Link URL should not be empty for '{text}'"
                    )
                    # Check URL format (basic validation)
                    if not url.startswith('#'):  # Skip anchor links
                        self.assertTrue(
                            url.startswith('http://') or
                            url.startswith('https://') or
                            url.startswith('/') or
                            url.endswith('.md') or
                            url.endswith('.png') or
                            url.endswith('.jpg') or
                            url.endswith('.svg'),
                            f"Link URL '{url}' should be valid"
                        )


class TestDocumentationConsistency(unittest.TestCase):
    """Test consistency between documentation and manifest"""

    @classmethod
    def setUpClass(cls):
        """Load all relevant files"""
        base_path = os.path.dirname(os.path.dirname(__file__))

        with open(os.path.join(base_path, 'manifest.json'), 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

        readme_path = os.path.join(base_path, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                cls.readme = f.read()
        else:
            cls.readme = ""

        changelog_path = os.path.join(base_path, 'CHANGELOG.md')
        if os.path.exists(changelog_path):
            with open(changelog_path, 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = ""

    def test_name_consistency(self):
        """Test that modpack name is consistent across files"""
        name = self.manifest.get('name')

        if self.readme:
            # Name should appear in README (case-insensitive)
            self.assertTrue(
                name.lower() in self.readme.lower() or
                name.replace('_', ' ').lower() in self.readme.lower(),
                f"Modpack name '{name}' should appear in README"
            )

    def test_description_consistency(self):
        """Test that description is consistent"""
        description = self.manifest.get('description')

        if self.readme and description:
            # Description or similar text should appear in README
            # Allow for minor variations
            desc_words = set(description.lower().split())
            readme_words = set(self.readme.lower().split())

            # At least 50% of description words should be in README
            overlap = len(desc_words & readme_words) / len(desc_words)
            self.assertGreater(
                overlap,
                0.5,
                "Description should be reflected in README"
            )

    def test_website_url_in_readme(self):
        """Test that website URL appears in README"""
        url = self.manifest.get('website_url')

        if self.readme and url:
            self.assertIn(
                url,
                self.readme,
                "Website URL from manifest should appear in README"
            )


if __name__ == '__main__':
    unittest.main()
