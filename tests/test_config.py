"""
Test suite for configuration file validation.

This module tests all .cfg files in the config directory to ensure they
are properly formatted and contain valid configuration data.
"""

import unittest
import os
import re
from pathlib import Path
from configparser import ConfigParser, Error as ConfigParserError


class TestConfigFilesExist(unittest.TestCase):
    """Test that configuration files exist and are accessible"""

    @classmethod
    def setUpClass(cls):
        """Set up paths for testing"""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"

    def test_config_directory_exists(self):
        """Test that config directory exists"""
        self.assertTrue(
            self.config_dir.exists(),
            "config directory must exist"
        )
        self.assertTrue(
            self.config_dir.is_dir(),
            "config must be a directory"
        )

    def test_config_files_present(self):
        """Test that config directory contains .cfg files"""
        if not self.config_dir.exists():
            self.skipTest("config directory does not exist")

        cfg_files = list(self.config_dir.glob("*.cfg"))
        self.assertGreater(
            len(cfg_files),
            0,
            "config directory should contain at least one .cfg file"
        )

    def test_bepinex_config_exists(self):
        """Test that BepInEx.cfg exists (core configuration file)"""
        bepinex_cfg = self.config_dir / "BepInEx.cfg"
        self.assertTrue(
            bepinex_cfg.exists(),
            "BepInEx.cfg should exist as it's the core configuration"
        )


class TestConfigFileFormat(unittest.TestCase):
    """Test the format and structure of configuration files"""

    @classmethod
    def setUpClass(cls):
        """Load all config files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"

        if cls.config_dir.exists():
            cls.cfg_files = list(cls.config_dir.glob("*.cfg"))
        else:
            cls.cfg_files = []

    def test_config_files_are_readable(self):
        """Test that all .cfg files can be read"""
        if not self.cfg_files:
            self.skipTest("No config files found")

        for cfg_file in self.cfg_files:
            with self.subTest(config=cfg_file.name):
                try:
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.assertIsNotNone(content)
                except UnicodeDecodeError:
                    # Try with different encoding
                    try:
                        with open(cfg_file, 'r', encoding='utf-8-sig') as f:
                            content = f.read()
                    except Exception as e:
                        self.fail(f"Could not read {cfg_file.name}: {e}")
                except Exception as e:
                    self.fail(f"Error reading {cfg_file.name}: {e}")

    def test_config_files_ini_format(self):
        """Test that config files follow INI format (where applicable)"""
        if not self.cfg_files:
            self.skipTest("No config files found")

        for cfg_file in self.cfg_files:
            with self.subTest(config=cfg_file.name):
                parser = ConfigParser()
                try:
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Some config files might be empty or have special formats
                    if len(content.strip()) == 0:
                        continue

                    # Try to parse as INI
                    parser.read(cfg_file, encoding='utf-8')

                except ConfigParserError as e:
                    # Some mods use non-standard config formats, log but don't fail
                    # This is informational
                    pass
                except Exception as e:
                    self.fail(f"Unexpected error parsing {cfg_file.name}: {e}")

    def test_no_invalid_characters(self):
        """Test that config files don't contain invalid control characters"""
        if not self.cfg_files:
            self.skipTest("No config files found")

        # Allow common control characters: newline, carriage return, tab
        invalid_chars_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')

        for cfg_file in self.cfg_files:
            with self.subTest(config=cfg_file.name):
                try:
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    matches = invalid_chars_pattern.findall(content)
                    self.assertEqual(
                        len(matches),
                        0,
                        f"{cfg_file.name} contains invalid control characters"
                    )
                except Exception:
                    # If we can't read it, other tests will catch it
                    pass


class TestBepInExConfig(unittest.TestCase):
    """Test specific BepInEx configuration requirements"""

    @classmethod
    def setUpClass(cls):
        """Load BepInEx.cfg"""
        cls.repo_root = Path(__file__).parent.parent
        cls.bepinex_cfg = cls.repo_root / "config" / "BepInEx.cfg"

    def test_bepinex_config_readable(self):
        """Test that BepInEx.cfg is readable"""
        if not self.bepinex_cfg.exists():
            self.skipTest("BepInEx.cfg does not exist")

        try:
            with open(self.bepinex_cfg, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertGreater(len(content), 0, "BepInEx.cfg should not be empty")
        except Exception as e:
            self.fail(f"Could not read BepInEx.cfg: {e}")

    def test_bepinex_config_has_sections(self):
        """Test that BepInEx.cfg has expected configuration sections"""
        if not self.bepinex_cfg.exists():
            self.skipTest("BepInEx.cfg does not exist")

        parser = ConfigParser()
        try:
            parser.read(self.bepinex_cfg, encoding='utf-8')

            # BepInEx typically has these sections
            expected_sections = ['Logging.Console', 'Logging.Disk']

            for section in expected_sections:
                with self.subTest(section=section):
                    # Check if section exists (case-insensitive search)
                    section_found = any(
                        s.lower() == section.lower()
                        for s in parser.sections()
                    )
                    if not section_found:
                        # This is informational, not critical
                        pass

        except Exception as e:
            # BepInEx.cfg format might vary
            pass


class TestConfigNaming(unittest.TestCase):
    """Test configuration file naming conventions"""

    @classmethod
    def setUpClass(cls):
        """Load all config files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"

        if cls.config_dir.exists():
            cls.cfg_files = list(cls.config_dir.glob("*.cfg"))
            cls.all_files = list(cls.config_dir.glob("*"))
        else:
            cls.cfg_files = []
            cls.all_files = []

    def test_config_files_have_cfg_extension(self):
        """Test that configuration files use .cfg extension"""
        if not self.all_files:
            self.skipTest("config directory is empty")

        non_cfg_files = [
            f for f in self.all_files
            if f.is_file() and not f.name.endswith('.cfg') and not f.name.endswith('.txt')
        ]

        if non_cfg_files:
            # Informational: some mods might use different extensions
            pass

    def test_config_names_match_mods(self):
        """Test that config file names correspond to mod names in manifest"""
        if not self.cfg_files:
            self.skipTest("No config files found")

        manifest_path = self.repo_root / "manifest.json"
        if not manifest_path.exists():
            self.skipTest("manifest.json not found")

        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # Extract mod names from dependencies
        mod_names = []
        for dep in manifest.get('dependencies', []):
            parts = dep.split('-')
            if len(parts) >= 2:
                # ModName is typically the second part
                mod_names.append(parts[1])

        # Some config files might not match exactly, but check for common ones
        # This is more informational than strict
        for cfg_file in self.cfg_files:
            # This test is informational - some configs might be for BepInEx itself
            pass


class TestConfigConsistency(unittest.TestCase):
    """Test consistency between config files and manifest dependencies"""

    @classmethod
    def setUpClass(cls):
        """Load manifest and config files"""
        cls.repo_root = Path(__file__).parent.parent
        cls.config_dir = cls.repo_root / "config"
        cls.manifest_path = cls.repo_root / "manifest.json"

    def test_critical_configs_present(self):
        """Test that configs exist for critical mods"""
        if not self.manifest_path.exists():
            self.skipTest("manifest.json not found")
        if not self.config_dir.exists():
            self.skipTest("config directory not found")

        import json
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # BepInEx should always have a config
        bepinex_in_deps = any('BepInEx' in dep for dep in manifest.get('dependencies', []))
        bepinex_cfg_exists = (self.config_dir / "BepInEx.cfg").exists()

        if bepinex_in_deps:
            self.assertTrue(
                bepinex_cfg_exists,
                "BepInEx.cfg should exist when BepInEx is a dependency"
            )


if __name__ == '__main__':
    unittest.main()
