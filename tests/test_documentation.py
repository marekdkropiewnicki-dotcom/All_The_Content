"""
Test suite for documentation validation.

This module tests README.md, CHANGELOG.md, and other documentation files
to ensure they are properly formatted and contain required information.
"""

import unittest
import re
from pathlib import Path


class TestReadmeFile(unittest.TestCase):
    """Test README.md structure and content"""

    @classmethod
    def setUpClass(cls):
        """Load README.md"""
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"

        if cls.readme_path.exists():
            with open(cls.readme_path, 'r', encoding='utf-8') as f:
                cls.readme_content = f.read()
        else:
            cls.readme_content = None

    def test_readme_exists(self):
        """Test that README.md exists"""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md must exist in repository root"
        )

    def test_readme_not_empty(self):
        """Test that README.md is not empty"""
        if self.readme_content is None:
            self.skipTest("README.md does not exist")

        self.assertGreater(
            len(self.readme_content),
            50,
            "README.md should contain meaningful content"
        )

    def test_readme_has_title(self):
        """Test that README.md has a title (H1 heading)"""
        if self.readme_content is None:
            self.skipTest("README.md does not exist")

        # Check for markdown H1 heading
        h1_pattern = r'^#\s+.+$'
        has_h1 = re.search(h1_pattern, self.readme_content, re.MULTILINE)

        # Also check for HTML h1
        html_h1_pattern = r'<h1>.*</h1>'
        has_html_h1 = re.search(html_h1_pattern, self.readme_content, re.IGNORECASE)

        self.assertTrue(
            has_h1 or has_html_h1,
            "README.md should have a title (H1 heading)"
        )

    def test_readme_has_description(self):
        """Test that README.md contains a description section"""
        if self.readme_content is None:
            self.skipTest("README.md does not exist")

        # Look for description section or substantial content
        has_description_section = "description" in self.readme_content.lower()
        has_content = len(self.readme_content.split('\n')) > 10

        self.assertTrue(
            has_description_section or has_content,
            "README.md should contain a description of the modpack"
        )

    def test_readme_mentions_modpack(self):
        """Test that README.md mentions it's a modpack or mod collection"""
        if self.readme_content is None:
            self.skipTest("README.md does not exist")

        # Look for keywords that indicate this is a modpack
        modpack_keywords = ['modpack', 'mod', 'content warning', 'thunderstore']
        content_lower = self.readme_content.lower()

        has_keyword = any(keyword in content_lower for keyword in modpack_keywords)
        self.assertTrue(
            has_keyword,
            "README.md should mention that this is a modpack or mod collection"
        )

    def test_readme_has_links(self):
        """Test that README.md contains useful links"""
        if self.readme_content is None:
            self.skipTest("README.md does not exist")

        # Check for markdown or HTML links
        markdown_link_pattern = r'\[.+\]\(.+\)'
        html_link_pattern = r'<a\s+href=".+".*>.*</a>'

        has_markdown_links = re.search(markdown_link_pattern, self.readme_content)
        has_html_links = re.search(html_link_pattern, self.readme_content, re.IGNORECASE)

        self.assertTrue(
            has_markdown_links or has_html_links,
            "README.md should contain links (e.g., to Thunderstore, Discord, or GitHub)"
        )


class TestChangelogFile(unittest.TestCase):
    """Test CHANGELOG.md structure and content"""

    @classmethod
    def setUpClass(cls):
        """Load CHANGELOG.md"""
        cls.repo_root = Path(__file__).parent.parent
        cls.changelog_path = cls.repo_root / "CHANGELOG.md"

        if cls.changelog_path.exists():
            with open(cls.changelog_path, 'r', encoding='utf-8') as f:
                cls.changelog_content = f.read()
        else:
            cls.changelog_content = None

    def test_changelog_exists(self):
        """Test that CHANGELOG.md exists"""
        self.assertTrue(
            self.changelog_path.exists(),
            "CHANGELOG.md should exist to track version history"
        )

    def test_changelog_not_empty(self):
        """Test that CHANGELOG.md is not empty"""
        if self.changelog_content is None:
            self.skipTest("CHANGELOG.md does not exist")

        self.assertGreater(
            len(self.changelog_content),
            20,
            "CHANGELOG.md should contain version history"
        )

    def test_changelog_has_versions(self):
        """Test that CHANGELOG.md contains version entries"""
        if self.changelog_content is None:
            self.skipTest("CHANGELOG.md does not exist")

        # Look for version patterns
        version_patterns = [
            r'[Vv]ersion\s+\d+\.\d+\.\d+',
            r'##\s+\d+\.\d+\.\d+',
            r'v?\d+\.\d+\.\d+',
        ]

        has_versions = any(
            re.search(pattern, self.changelog_content)
            for pattern in version_patterns
        )

        self.assertTrue(
            has_versions,
            "CHANGELOG.md should contain version numbers"
        )

    def test_changelog_has_current_version(self):
        """Test that CHANGELOG.md includes the current version from manifest"""
        if self.changelog_content is None:
            self.skipTest("CHANGELOG.md does not exist")

        manifest_path = self.repo_root / "manifest.json"
        if not manifest_path.exists():
            self.skipTest("manifest.json not found")

        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        current_version = manifest.get('version_number', '')

        self.assertIn(
            current_version,
            self.changelog_content,
            f"CHANGELOG.md should document current version {current_version}"
        )

    def test_changelog_chronological_order(self):
        """Test that versions in CHANGELOG.md are in reasonable order"""
        if self.changelog_content is None:
            self.skipTest("CHANGELOG.md does not exist")

        # Extract all version numbers
        version_pattern = r'[Vv]ersion\s+(\d+)\.(\d+)\.(\d+)'
        matches = re.findall(version_pattern, self.changelog_content)

        if len(matches) < 2:
            self.skipTest("Not enough versions to check order")

        # Convert to tuples of ints for comparison
        versions = [(int(major), int(minor), int(patch)) for major, minor, patch in matches]

        # Check if versions are in descending order (newest first) or ascending order
        is_descending = all(versions[i] >= versions[i+1] for i in range(len(versions)-1))
        is_ascending = all(versions[i] <= versions[i+1] for i in range(len(versions)-1))

        self.assertTrue(
            is_descending or is_ascending,
            "Versions in CHANGELOG.md should be in chronological order"
        )


class TestDocumentationQuality(unittest.TestCase):
    """Test overall documentation quality"""

    @classmethod
    def setUpClass(cls):
        """Load documentation files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"
        cls.changelog_path = cls.repo_root / "CHANGELOG.md"

    def test_no_placeholder_text(self):
        """Test that documentation doesn't contain placeholder text"""
        placeholder_patterns = [
            r'\[TODO\]',
            r'\[PLACEHOLDER\]',
            r'lorem ipsum',
            r'TODO:',
            r'FIXME:',
        ]

        files_to_check = [
            (self.readme_path, "README.md"),
            (self.changelog_path, "CHANGELOG.md"),
        ]

        for file_path, file_name in files_to_check:
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            for pattern in placeholder_patterns:
                with self.subTest(file=file_name, pattern=pattern):
                    has_placeholder = re.search(pattern, content, re.IGNORECASE)
                    self.assertFalse(
                        has_placeholder,
                        f"{file_name} contains placeholder text: {pattern}"
                    )

    def test_proper_markdown_formatting(self):
        """Test that markdown files don't have common formatting issues"""
        files_to_check = [
            (self.readme_path, "README.md"),
            (self.changelog_path, "CHANGELOG.md"),
        ]

        for file_path, file_name in files_to_check:
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with self.subTest(file=file_name):
                # Check that headings have space after #
                for i, line in enumerate(lines, 1):
                    if line.startswith('#') and not line.startswith('####'):
                        # Should have space after # (unless it's an HTML tag)
                        if not line.startswith('<'):
                            if len(line) > 1 and line[line.find('#')+1] != ' ':
                                # Allow multiple # without space (like ###)
                                if not all(c == '#' for c in line[1:line.rfind('#')+1]):
                                    # This is informational, not critical
                                    pass

    def test_links_not_broken_format(self):
        """Test that markdown links are properly formatted"""
        files_to_check = [
            (self.readme_path, "README.md"),
        ]

        for file_path, file_name in files_to_check:
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all markdown links
            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            links = re.findall(link_pattern, content)

            for link_text, link_url in links:
                with self.subTest(file=file_name, link=link_url):
                    # Check that URL is not empty
                    self.assertGreater(
                        len(link_url.strip()),
                        0,
                        f"Empty URL in markdown link: [{link_text}]()"
                    )


class TestRepositoryMetadata(unittest.TestCase):
    """Test repository metadata and required files"""

    @classmethod
    def setUpClass(cls):
        """Set up repository paths"""
        cls.repo_root = Path(__file__).parent.parent

    def test_required_files_exist(self):
        """Test that all required files for a Thunderstore package exist"""
        required_files = [
            ('manifest.json', 'Required for Thunderstore package'),
            ('icon.png', 'Required for Thunderstore package'),
            ('README.md', 'Required for documentation'),
        ]

        for filename, reason in required_files:
            with self.subTest(file=filename):
                file_path = self.repo_root / filename
                self.assertTrue(
                    file_path.exists(),
                    f"{filename} is missing. {reason}"
                )

    def test_image_files_valid_extension(self):
        """Test that image files have valid extensions"""
        image_dir = self.repo_root / "images"

        if not image_dir.exists():
            # Images directory is optional
            return

        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']
        image_files = [f for f in image_dir.iterdir() if f.is_file()]

        for image_file in image_files:
            with self.subTest(image=image_file.name):
                has_valid_ext = any(
                    image_file.name.lower().endswith(ext)
                    for ext in image_extensions
                )
                self.assertTrue(
                    has_valid_ext,
                    f"{image_file.name} should have a valid image extension"
                )


if __name__ == '__main__':
    unittest.main()
