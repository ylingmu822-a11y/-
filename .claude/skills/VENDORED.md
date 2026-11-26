# Vendored: academic-research-skills

- Source: https://github.com/Imbad0202/academic-research-skills
- Commit: 96925d2ab5f2f5d82cbffe7bada8fce163c6bfb4 (plugin v3.24.5)
- License: CC-BY-NC-4.0 (see LICENSE / NOTICE.md in this directory)

Installed by copying instead of `/plugin install`, because `/plugin` is unavailable
in Claude Code cloud sessions.

Layout (mirrors the plugin root so relative `../shared/...` links keep working):
- `.claude/skills/{deep-research,academic-paper,academic-paper-reviewer,academic-pipeline,sr-screener}` — skills
- `.claude/skills/{shared,agents,docs,scripts,MODE_REGISTRY.md}` — supporting files
- `.claude/agents/` — the 4 plugin subagents
- `.claude/commands/` — the `/ars-*` slash commands

`${CLAUDE_PLUGIN_ROOT}` was rewritten to `.claude/skills`. Plugin hooks (optional
write-scope guard, load announcement) were not installed. Test files and fixtures
under `scripts/` were omitted.
