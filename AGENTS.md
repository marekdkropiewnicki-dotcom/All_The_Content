# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **Thunderstore modpack** for the video game *Content Warning*. It is marked as **[DEPRECATED]**.

- **No source code, build system, tests, or runnable services exist.** The entire repo is a declarative modpack definition: a JSON manifest (`manifest.json`), BepInEx config files (`config/*.cfg`), and image assets.
- There are **no dependencies to install**, no package manager, and no dev server to run.
- The only meaningful validation is checking that `manifest.json` is valid JSON with correctly formatted Thunderstore dependency strings (`Author-ModName-X.Y.Z`), and that config/image files are present and non-empty.
- To validate the manifest: `python3 -c "import json; json.load(open('manifest.json'))"`
- Lint/test/build commands: **none exist**. There is no CI configuration.
