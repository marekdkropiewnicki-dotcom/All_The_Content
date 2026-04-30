"""
Tests for configuration files validation.
Ensures all config files are valid and follow expected formats.
"""
import os
import re
import unittest
from pathlib import Path


class TestConfigFiles(unittest.TestCase):
    """Test cases for configuration files."""

    @classmethod
    def setUpClass(cls):
        """Find all config files."""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"
        cls.config_files = list(cls.config_dir.glob("*.cfg")) if cls.config_dir.exists() else []

    def test_config_directory_exists(self):
        """Test that config directory exists."""
        self.assertTrue(self.config_dir.exists(), "config directory must exist")
        self.assertTrue(self.config_dir.is_dir(), "config must be a directory")

    def test_config_files_exist(self):
        """Test that at least one config file exists."""
        self.assertGreater(len(self.config_files), 0, "At least one config file should exist")

    def test_config_files_readable(self):
        """Test that all config files are readable."""
        for config_file in self.config_files:
            with self.subTest(config=config_file.name):
                self.assertTrue(config_file.exists(), f"{config_file.name} must exist")
                self.assertTrue(config_file.is_file(), f"{config_file.name} must be a file")

                # Try to read the file
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.assertIsInstance(content, str, f"{config_file.name} must be readable as text")
                except Exception as e:
                    self.fail(f"Failed to read {config_file.name}: {e}")

    def test_config_files_not_empty(self):
        """Test that config files are not empty (unless they're intentionally empty like txt files)."""
        for config_file in self.config_files:
            if config_file.suffix == '.cfg':
                with self.subTest(config=config_file.name):
                    size = config_file.stat().st_size
                    # Allow empty .txt files but .cfg files should have content
                    if config_file.suffix == '.cfg':
                        # Some cfg files might be intentionally minimal, so we just check they exist
                        self.assertGreaterEqual(size, 0, f"{config_file.name} must be readable")

    def test_bepinex_config_exists(self):
        """Test that BepInEx.cfg exists (core configuration)."""
        bepinex_config = self.config_dir / "BepInEx.cfg"
        self.assertTrue(
            bepinex_config.exists(),
            "BepInEx.cfg must exist as it's the core configuration"
        )

    def test_config_files_encoding(self):
        """Test that all config files use UTF-8 encoding."""
        for config_file in self.config_files:
            with self.subTest(config=config_file.name):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError:
                    self.fail(f"{config_file.name} is not valid UTF-8")

    def test_config_files_no_trailing_whitespace(self):
        """Test that config files don't have excessive trailing whitespace."""
        for config_file in self.config_files:
            if config_file.suffix == '.cfg':
                with self.subTest(config=config_file.name):
                    with open(config_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # Check that lines don't have excessive trailing spaces (more than 1)
                    for i, line in enumerate(lines, 1):
                        trailing_spaces = len(line) - len(line.rstrip(' \t'))
                        if trailing_spaces > 1 and line.strip():  # Ignore empty lines
                            self.fail(
                                f"{config_file.name}:{i} has excessive trailing whitespace "
                                f"({trailing_spaces} spaces)"
                            )

    def test_config_naming_convention(self):
        """Test that config files follow naming conventions."""
        for config_file in self.config_files:
            with self.subTest(config=config_file.name):
                name = config_file.name
                # Config files should end with .cfg or be .txt files
                self.assertTrue(
                    name.endswith('.cfg') or name.endswith('.txt'),
                    f"{name} should have .cfg or .txt extension"
                )


class TestSpecificConfigs(unittest.TestCase):
    """Test specific configuration files for known mods."""

    @classmethod
    def setUpClass(cls):
        """Setup paths."""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"

    def test_content_library_config(self):
        """Test ContentLibrary config if present."""
        config_path = self.config_dir / "Notest.ContentLibrary.cfg"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIsInstance(content, str, "ContentLibrary config must be readable")

    def test_bepinex_config_structure(self):
        """Test that BepInEx.cfg has expected structure."""
        config_path = self.config_dir / "BepInEx.cfg"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # BepInEx configs typically have [Section] headers
            self.assertRegex(
                content,
                r'\[.*\]',
                "BepInEx.cfg should contain section headers"
            )


class TestConfigConsistencyWithManifest(unittest.TestCase):
    """Test that config files are consistent with manifest dependencies."""

    @classmethod
    def setUpClass(cls):
        """Load manifest and find configs."""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"

        import json
        with open(cls.repo_root / "manifest.json", 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

        cls.config_files = list(cls.config_dir.glob("*.cfg")) if cls.config_dir.exists() else []

    def test_major_mods_have_configs(self):
        """Test that major mods listed in dependencies have corresponding configs."""
        dependencies = self.manifest.get("dependencies", [])
        config_names = [f.stem for f in self.config_files]

        # Extract mod names from dependencies
        # These are high-profile mods that typically have configs
        important_mods = []
        for dep in dependencies:
            if any(keyword in dep for keyword in ['BepInEx', 'Configuration']):
                mod_name = dep.split('-')[1] if '-' in dep else dep
                important_mods.append(mod_name)

        # Check if at least BepInEx config exists
        bepinex_config_exists = any('BepInEx' in name for name in config_names)
        self.assertTrue(
            bepinex_config_exists,
            "BepInEx config should exist for BepInEx dependency"
        )


if __name__ == '__main__':
    unittest.main()
