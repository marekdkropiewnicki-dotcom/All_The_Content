"""
Tests for manifest.json validation
"""
import json
import os
import re
import unittest


class TestManifest(unittest.TestCase):
    """Test suite for validating manifest.json"""

    @classmethod
    def setUpClass(cls):
        """Load the manifest file once for all tests"""
        cls.manifest_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'manifest.json'
        )
        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_manifest_exists(self):
        """Test that manifest.json exists"""
        self.assertTrue(
            os.path.exists(self.manifest_path),
            "manifest.json file must exist"
        )

    def test_manifest_valid_json(self):
        """Test that manifest.json is valid JSON"""
        self.assertIsInstance(self.manifest, dict, "Manifest must be a JSON object")

    def test_required_fields_present(self):
        """Test that all required Thunderstore fields are present"""
        required_fields = ['name', 'version_number', 'website_url', 'description', 'dependencies']
        for field in required_fields:
            self.assertIn(
                field,
                self.manifest,
                f"Required field '{field}' must be present in manifest.json"
            )

    def test_name_valid(self):
        """Test that name field is valid"""
        name = self.manifest.get('name')
        self.assertIsInstance(name, str, "Name must be a string")
        self.assertTrue(len(name) > 0, "Name cannot be empty")
        self.assertTrue(len(name) <= 256, "Name must be 256 characters or less")

    def test_version_number_format(self):
        """Test that version_number follows semantic versioning (X.Y.Z)"""
        version = self.manifest.get('version_number')
        self.assertIsInstance(version, str, "Version number must be a string")

        # Test semantic versioning format
        version_pattern = r'^\d+\.\d+\.\d+$'
        self.assertIsNotNone(
            re.match(version_pattern, version),
            f"Version '{version}' must follow semantic versioning format (X.Y.Z)"
        )

    def test_website_url_valid(self):
        """Test that website_url is a valid URL"""
        url = self.manifest.get('website_url')
        self.assertIsInstance(url, str, "Website URL must be a string")
        self.assertTrue(
            url.startswith('http://') or url.startswith('https://'),
            "Website URL must start with http:// or https://"
        )

    def test_description_valid(self):
        """Test that description is valid"""
        description = self.manifest.get('description')
        self.assertIsInstance(description, str, "Description must be a string")
        self.assertTrue(len(description) > 0, "Description cannot be empty")
        self.assertTrue(
            len(description) <= 250,
            "Description must be 250 characters or less"
        )

    def test_dependencies_is_list(self):
        """Test that dependencies field is a list"""
        dependencies = self.manifest.get('dependencies')
        self.assertIsInstance(dependencies, list, "Dependencies must be a list")

    def test_dependencies_format(self):
        """Test that each dependency follows the format Author-ModName-Version"""
        dependencies = self.manifest.get('dependencies', [])
        dependency_pattern = r'^[^-]+-[^-]+-\d+\.\d+\.\d+$'

        for dep in dependencies:
            self.assertIsInstance(dep, str, f"Dependency '{dep}' must be a string")
            self.assertIsNotNone(
                re.match(dependency_pattern, dep),
                f"Dependency '{dep}' must follow format 'Author-ModName-Version'"
            )

    def test_bepinex_dependency_present(self):
        """Test that BepInEx is listed as a dependency"""
        dependencies = self.manifest.get('dependencies', [])
        bepinex_found = any('BepInEx' in dep for dep in dependencies)
        self.assertTrue(
            bepinex_found,
            "BepInEx must be listed as a dependency for modpacks"
        )

    def test_no_duplicate_dependencies(self):
        """Test that there are no duplicate dependencies"""
        dependencies = self.manifest.get('dependencies', [])
        self.assertEqual(
            len(dependencies),
            len(set(dependencies)),
            "Dependencies list must not contain duplicates"
        )

    def test_dependency_versions_valid(self):
        """Test that all dependency versions are valid semantic versions"""
        dependencies = self.manifest.get('dependencies', [])

        for dep in dependencies:
            parts = dep.split('-')
            if len(parts) >= 3:
                version = parts[-1]
                version_pattern = r'^\d+\.\d+\.\d+$'
                self.assertIsNotNone(
                    re.match(version_pattern, version),
                    f"Version in dependency '{dep}' must be semantic (X.Y.Z)"
                )


class TestManifestConsistency(unittest.TestCase):
    """Test suite for checking consistency with other files"""

    @classmethod
    def setUpClass(cls):
        """Load manifest and README"""
        base_path = os.path.dirname(os.path.dirname(__file__))

        with open(os.path.join(base_path, 'manifest.json'), 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

        readme_path = os.path.join(base_path, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                cls.readme = f.read()
        else:
            cls.readme = ""

    def test_version_in_readme(self):
        """Test that the current version is mentioned in README"""
        version = self.manifest.get('version_number')
        if self.readme:
            # Version might be in changelog or elsewhere
            self.assertIn(
                version,
                self.readme,
                f"Version {version} should be documented in README.md"
            )


if __name__ == '__main__':
    unittest.main()
