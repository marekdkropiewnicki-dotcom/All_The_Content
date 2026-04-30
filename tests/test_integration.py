"""
Integration tests for the entire modpack structure
"""
import json
import os
import unittest


class TestModpackStructure(unittest.TestCase):
    """Test suite for validating overall modpack structure"""

    @classmethod
    def setUpClass(cls):
        """Set up paths and load manifest"""
        cls.base_path = os.path.dirname(os.path.dirname(__file__))

        with open(os.path.join(cls.base_path, 'manifest.json'), 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_required_files_exist(self):
        """Test that all required Thunderstore files exist"""
        required_files = [
            'manifest.json',
            'README.md',
            'icon.png'
        ]

        for file_name in required_files:
            file_path = os.path.join(self.base_path, file_name)
            with self.subTest(file=file_name):
                self.assertTrue(
                    os.path.exists(file_path),
                    f"Required file '{file_name}' must exist"
                )

    def test_icon_is_valid(self):
        """Test that icon.png is a valid image file"""
        icon_path = os.path.join(self.base_path, 'icon.png')

        if os.path.exists(icon_path):
            # Check file size is reasonable (between 1KB and 5MB)
            size = os.path.getsize(icon_path)
            self.assertGreater(
                size,
                1024,
                "icon.png should be larger than 1KB"
            )
            self.assertLess(
                size,
                5 * 1024 * 1024,
                "icon.png should be smaller than 5MB"
            )

            # Check PNG header
            with open(icon_path, 'rb') as f:
                header = f.read(8)
                # PNG magic number: 89 50 4E 47 0D 0A 1A 0A
                self.assertEqual(
                    header,
                    b'\x89PNG\r\n\x1a\n',
                    "icon.png must have valid PNG header"
                )

    def test_no_sensitive_files(self):
        """Test that no sensitive files are present"""
        sensitive_patterns = [
            '.env',
            'credentials',
            'secrets',
            'password',
            'private_key',
            'id_rsa'
        ]

        all_files = []
        for root, dirs, files in os.walk(self.base_path):
            # Skip .git directory
            if '.git' in root:
                continue
            all_files.extend([os.path.join(root, f) for f in files])

        for file_path in all_files:
            file_name = os.path.basename(file_path).lower()
            with self.subTest(file=file_name):
                for pattern in sensitive_patterns:
                    self.assertNotIn(
                        pattern,
                        file_name,
                        f"Sensitive file pattern '{pattern}' found in '{file_name}'"
                    )

    def test_modpack_size_reasonable(self):
        """Test that modpack size is reasonable for distribution"""
        total_size = 0

        for root, dirs, files in os.walk(self.base_path):
            # Skip .git directory
            if '.git' in root:
                continue

            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)

        # Modpack should be less than 50MB (excluding .git)
        max_size = 50 * 1024 * 1024
        self.assertLess(
            total_size,
            max_size,
            f"Modpack size {total_size / 1024 / 1024:.2f}MB exceeds recommended {max_size / 1024 / 1024:.2f}MB"
        )


class TestDependencyIntegrity(unittest.TestCase):
    """Test dependency relationships and integrity"""

    @classmethod
    def setUpClass(cls):
        """Load manifest"""
        base_path = os.path.dirname(os.path.dirname(__file__))

        with open(os.path.join(base_path, 'manifest.json'), 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_dependency_count_reasonable(self):
        """Test that dependency count is reasonable"""
        dependencies = self.manifest.get('dependencies', [])

        # Should have at least BepInEx
        self.assertGreater(
            len(dependencies),
            0,
            "Should have at least one dependency (BepInEx)"
        )

        # Shouldn't have too many (arbitrary limit for sanity)
        self.assertLess(
            len(dependencies),
            200,
            "Dependency count seems unreasonably high"
        )

    def test_all_dependencies_unique_mods(self):
        """Test that each mod appears only once in dependencies"""
        dependencies = self.manifest.get('dependencies', [])

        # Extract mod names (Author-ModName part)
        mod_names = []
        for dep in dependencies:
            parts = dep.rsplit('-', 1)  # Split from right, version is last
            if len(parts) >= 1:
                mod_names.append(parts[0])

        self.assertEqual(
            len(mod_names),
            len(set(mod_names)),
            "Each mod should appear only once (no duplicate mods with different versions)"
        )


if __name__ == '__main__':
    unittest.main()
