"""
Tests for configuration files validation
"""
import os
import unittest


class TestConfigFiles(unittest.TestCase):
    """Test suite for validating configuration files"""

    @classmethod
    def setUpClass(cls):
        """Set up paths to config directory"""
        cls.config_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config'
        )

    def test_config_directory_exists(self):
        """Test that config directory exists"""
        self.assertTrue(
            os.path.exists(self.config_dir),
            "config directory must exist"
        )
        self.assertTrue(
            os.path.isdir(self.config_dir),
            "config must be a directory"
        )

    def test_config_files_exist(self):
        """Test that config directory contains .cfg files"""
        if os.path.exists(self.config_dir):
            cfg_files = [f for f in os.listdir(self.config_dir) if f.endswith('.cfg')]
            self.assertGreater(
                len(cfg_files),
                0,
                "config directory should contain at least one .cfg file"
            )

    def test_config_files_readable(self):
        """Test that all .cfg files are readable"""
        if not os.path.exists(self.config_dir):
            self.skipTest("Config directory does not exist")

        cfg_files = [f for f in os.listdir(self.config_dir) if f.endswith('.cfg')]

        for cfg_file in cfg_files:
            file_path = os.path.join(self.config_dir, cfg_file)
            with self.subTest(file=cfg_file):
                self.assertTrue(
                    os.path.isfile(file_path),
                    f"{cfg_file} must be a file"
                )
                # Test that file can be opened and read
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.assertIsInstance(content, str)
                except Exception as e:
                    self.fail(f"Failed to read {cfg_file}: {e}")

    def test_bepinex_config_exists(self):
        """Test that BepInEx.cfg exists"""
        bepinex_config = os.path.join(self.config_dir, 'BepInEx.cfg')
        if os.path.exists(self.config_dir):
            self.assertTrue(
                os.path.exists(bepinex_config),
                "BepInEx.cfg must exist in config directory"
            )

    def test_config_files_not_empty(self):
        """Test that config files are not empty"""
        if not os.path.exists(self.config_dir):
            self.skipTest("Config directory does not exist")

        cfg_files = [f for f in os.listdir(self.config_dir) if f.endswith('.cfg')]

        for cfg_file in cfg_files:
            file_path = os.path.join(self.config_dir, cfg_file)
            with self.subTest(file=cfg_file):
                size = os.path.getsize(file_path)
                # Allow empty files for certain configs that might be intentionally empty
                if not cfg_file.endswith('.Backgrounds.txt'):
                    self.assertGreater(
                        size,
                        0,
                        f"{cfg_file} should not be empty (unless intentionally so)"
                    )

    def test_config_encoding_utf8(self):
        """Test that config files can be read as UTF-8"""
        if not os.path.exists(self.config_dir):
            self.skipTest("Config directory does not exist")

        cfg_files = [f for f in os.listdir(self.config_dir) if f.endswith('.cfg')]

        for cfg_file in cfg_files:
            file_path = os.path.join(self.config_dir, cfg_file)
            with self.subTest(file=cfg_file):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError:
                    self.fail(f"{cfg_file} must be valid UTF-8")


class TestConfigConsistency(unittest.TestCase):
    """Test consistency between config files and manifest"""

    @classmethod
    def setUpClass(cls):
        """Load manifest and config files"""
        import json

        base_path = os.path.dirname(os.path.dirname(__file__))
        cls.config_dir = os.path.join(base_path, 'config')

        with open(os.path.join(base_path, 'manifest.json'), 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_bepinex_config_matches_dependency(self):
        """Test that BepInEx config exists if BepInEx is a dependency"""
        dependencies = self.manifest.get('dependencies', [])
        has_bepinex = any('BepInEx' in dep for dep in dependencies)

        if has_bepinex and os.path.exists(self.config_dir):
            bepinex_config = os.path.join(self.config_dir, 'BepInEx.cfg')
            self.assertTrue(
                os.path.exists(bepinex_config),
                "BepInEx.cfg should exist when BepInEx is a dependency"
            )


if __name__ == '__main__':
    unittest.main()
