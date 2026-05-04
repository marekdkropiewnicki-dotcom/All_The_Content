# AGENTS.md

> **⚠️ DEPRECATED REPOSITORY**
>
> This modpack is **deprecated** and is no longer actively maintained. Do not invest effort in adding new features, restructuring the project, or modernizing tooling. Limit changes to small, well-justified fixes (e.g., correcting a broken dependency string, fixing a typo, or clarifying documentation). When in doubt, prefer doing nothing over making speculative changes.

## Cursor Cloud specific instructions

This repository is a **Thunderstore modpack** for the video game *Content Warning*.

- **No source code, build system, tests, or runnable services exist.** The entire repo is a declarative modpack definition: a JSON manifest (`manifest.json`), BepInEx config files (`config/*.cfg`), and image assets.
- There are **no dependencies to install**, no package manager, and no dev server to run.
- The only meaningful validation is checking that `manifest.json` is valid JSON with correctly formatted Thunderstore dependency strings (`Author-ModName-X.Y.Z`), and that config/image files are present and non-empty.
- To validate the manifest: `python3 -c "import json; json.load(open('manifest.json'))"`
- Lint/test/build commands: **none exist**. There is no CI configuration.
