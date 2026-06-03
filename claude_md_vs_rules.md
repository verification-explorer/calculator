# CLAUDE.md vs .claude/rules/ — Project Structure

## File Layout

```
calculator/
├── CLAUDE.md                  ← project overview, architecture, commands
├── CLAUDE.local.md            ← your venv rule (local only, gitignored)
├── .claude/
│   └── rules/
│       ├── gui.md             ← loads only when touching gui.py / programmer.py
│       ├── testing.md         ← loads only when touching tests/*.py
│       └── core.md            ← loads only when touching core logic files
```

## The Difference

| Use `CLAUDE.md` for | Use `.claude/rules/` for |
|---|---|
| Project overview, architecture | Specific dos and don'ts |
| Commands to run | Path-scoped constraints |
| Tech stack facts | Things that only apply to certain files |
| "What is this project" | "How to behave in this part of the project" |

## Key Concepts

- **CLAUDE.md** loads every session, always
- **Rules without `paths:`** also load every session, same as CLAUDE.md
- **Rules with `paths:`** only load when Claude opens a matching file — saves context tokens
- **CLAUDE.local.md** is personal, gitignored — never shared with the team

## What Makes a Rule Path-Scoped

The `---` frontmatter block at the top of a rule file:

```markdown
---
paths:
  - "src/calculator/gui.py"
  - "tests/*.py"
---

# Your rules here
```

Without the frontmatter, the rule loads every session.
With it, it only loads when Claude touches a matching file.
