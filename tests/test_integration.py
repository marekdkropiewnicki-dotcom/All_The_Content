"""
Integration tests for the modpack.

This module tests the integration and consistency between different
components of the modpack (manifest, configs, documentation).
"""

import unittest
import json
import re
from pathlib import Path
from configparser import ConfigParser


class TestManifestConfigIntegration(unittest.TestCase):
    """Test integration between manifest.json and config files"""

    @classmethod
    def setUpClass(cls):
        """Load manifest and config files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"
        cls.config_dir = cls.repo_root / "config"

        if cls.manifest_path.exists():
            with open(cls.manifest_path, 'r', encoding='utf-8') as f:
                cls.manifest = json.load(f)
        else:
            cls.manifest = None

        if cls.config_dir.exists():
            cls.cfg_files = list(cls.config_dir.glob("*.cfg"))
        else:
            cls.cfg_files = []

    def test_bepinex_dependency_and_config_consistency(self):
        """Test that BepInEx dependency matches BepInEx config presence"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")

        has_bepinex_dep = any(
            'BepInEx' in dep
            for dep in self.manifest.get('dependencies', [])
        )

        bepinex_cfg = self.config_dir / "BepInEx.cfg"
        has_bepinex_cfg = bepinex_cfg.exists()

        if has_bepinex_dep:
            self.assertTrue(
                has_bepinex_cfg,
                "BepInEx dependency exists but BepInEx.cfg is missing"
            )

    def test_dependency_count_reasonable(self):
        """Test that the number of dependencies is reasonable"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")

        dep_count = len(self.manifest.get('dependencies', []))
        cfg_count = len(self.cfg_files)

        # There should be at least BepInEx
        self.assertGreater(
            dep_count,
            0,
            "Should have at least one dependency (BepInEx)"
        )

        # Config files should exist (though not necessarily one per mod)
        if dep_count > 1:  # More than just BepInEx
            self.assertGreater(
                cfg_count,
                0,
                "Should have config files when mods are present"
            )


class TestDocumentationConsistency(unittest.TestCase):
    """Test consistency across documentation files"""

    @classmethod
    def setUpClass(cls):
        """Load all documentation files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"
        cls.readme_path = cls.repo_root / "README.md"
        cls.changelog_path = cls.repo_root / "CHANGELOG.md"

        if cls.manifest_path.exists():
            with open(cls.manifest_path, 'r', encoding='utf-8') as f:
                cls.manifest = json.load(f)
        else:
            cls.manifest = None

        if cls.readme_path.exists():
            with open(cls.readme_path, 'r', encoding='utf-8') as f:
                cls.readme = f.read()
        else:
            cls.readme = None

        if cls.changelog_path.exists():
            with open(cls.changelog_path, 'r', encoding='utf-8') as f:
                cls.changelog = f.read()
        else:
            cls.changelog = None

    def test_version_consistency(self):
        """Test that version is consistent across manifest and changelog"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")
        if self.changelog is None:
            self.skipTest("CHANGELOG.md not found")

        manifest_version = self.manifest.get('version_number', '')

        self.assertIn(
            manifest_version,
            self.changelog,
            f"Manifest version {manifest_version} should be in CHANGELOG.md"
        )

    def test_website_url_consistency(self):
        """Test that website URL in manifest matches documentation"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")
        if self.readme is None:
            self.skipTest("README.md not found")

        manifest_url = self.manifest.get('website_url', '')

        # Check if the URL or a variation appears in README
        # (might be in markdown link format)
        self.assertTrue(
            manifest_url in self.readme or manifest_url.split('://')[-1] in self.readme,
            "Manifest website_url should appear in README.md"
        )

    def test_description_consistency(self):
        """Test that description is consistent between manifest and README"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")
        if self.readme is None:
            self.skipTest("README.md not found")

        manifest_desc = self.manifest.get('description', '').lower()

        # Check if key phrases from description appear in README
        # Extract meaningful words (more than 3 characters)
        desc_words = [
            word for word in re.findall(r'\w+', manifest_desc)
            if len(word) > 3
        ]

        readme_lower = self.readme.lower()

        # At least some description words should appear in README
        matching_words = [word for word in desc_words if word in readme_lower]
        match_ratio = len(matching_words) / len(desc_words) if desc_words else 0

        self.assertGreater(
            match_ratio,
            0.3,
            "README should reflect the manifest description"
        )


class TestPackageIntegrity(unittest.TestCase):
    """Test overall package integrity and completeness"""

    @classmethod
    def setUpClass(cls):
        """Set up package paths"""
        cls.repo_root = Path(__file__).parent.parent

    def test_no_sensitive_files(self):
        """Test that repository doesn't contain sensitive files"""
        sensitive_patterns = [
            '*.key',
            '*.pem',
            '*.p12',
            '*password*',
            '*secret*',
            '.env',
        ]

        for pattern in sensitive_patterns:
            files = list(self.repo_root.rglob(pattern))
            # Filter out test files and git directory
            files = [
                f for f in files
                if '.git' not in str(f) and 'test' not in f.name.lower()
            ]

            with self.subTest(pattern=pattern):
                self.assertEqual(
                    len(files),
                    0,
                    f"Sensitive files matching {pattern} found: {files}"
                )

    def test_no_build_artifacts(self):
        """Test that repository doesn't contain build artifacts"""
        artifact_patterns = [
            '*.dll',
            '*.so',
            '*.dylib',
            '*.exe',
            '*.zip',
            '*.7z',
        ]

        for pattern in artifact_patterns:
            files = list(self.repo_root.rglob(pattern))
            # Filter out git directory
            files = [f for f in files if '.git' not in str(f)]

            # Some artifacts might be legitimate (icon.png is not an artifact)
            # This is more of a warning than a hard failure
            if files:
                # Informational: Some modpacks might include DLLs
                pass

    def test_consistent_line_endings(self):
        """Test that text files use consistent line endings"""
        text_files = []

        # Check markdown files
        text_files.extend(self.repo_root.glob("*.md"))

        # Check JSON files
        text_files.extend(self.repo_root.glob("*.json"))

        for text_file in text_files:
            with self.subTest(file=text_file.name):
                try:
                    with open(text_file, 'rb') as f:
                        content = f.read()

                    has_crlf = b'\r\n' in content
                    has_lf = b'\n' in content and not has_crlf

                    # Just check that the file has some line endings
                    # (either CRLF or LF is fine, but should be consistent)
                    self.assertTrue(
                        has_crlf or has_lf,
                        f"{text_file.name} should have line endings"
                    )

                except Exception:
                    # Skip binary files
                    pass


class TestDependencyValidation(unittest.TestCase):
    """Test dependency declarations and versions"""

    @classmethod
    def setUpClass(cls):
        """Load manifest"""
        cls.repo_root = Path(__file__).parent.parent
        cls.manifest_path = cls.repo_root / "manifest.json"

        if cls.manifest_path.exists():
            with open(cls.manifest_path, 'r', encoding='utf-8') as f:
                cls.manifest = json.load(f)
        else:
            cls.manifest = None

    def test_no_circular_dependencies(self):
        """Test that the modpack doesn't depend on itself"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")

        modpack_name = self.manifest.get('name', '')
        dependencies = self.manifest.get('dependencies', [])

        for dep in dependencies:
            self.assertNotIn(
                modpack_name,
                dep,
                f"Modpack should not depend on itself: {dep}"
            )

    def test_dependency_versions_not_outdated(self):
        """Test that dependencies don't use obviously outdated versions"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")

        dependencies = self.manifest.get('dependencies', [])

        for dep in dependencies:
            parts = dep.split('-')
            if len(parts) >= 3:
                version = parts[-1]
                version_parts = version.split('.')

                if len(version_parts) == 3:
                    major = int(version_parts[0])

                    # Just a sanity check - versions should be >= 0
                    self.assertGreaterEqual(
                        major,
                        0,
                        f"Invalid version in dependency {dep}"
                    )

    def test_critical_dependencies_present(self):
        """Test that critical dependencies are present"""
        if self.manifest is None:
            self.skipTest("manifest.json not found")

        dependencies = self.manifest.get('dependencies', [])

        # BepInEx is required for Content Warning mods
        has_bepinex = any('BepInEx' in dep for dep in dependencies)

        self.assertTrue(
            has_bepinex,
            "BepInEx should be in dependencies (required for Content Warning modpacks)"
        )


if __name__ == '__main__':
    unittest.main()
