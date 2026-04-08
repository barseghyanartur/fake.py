---
name: update-documentation
description: Sync fake.py project documentation with source code. Scans code and docs, finds misalignments, and auto-fixes them. Pure agent-based - no Python scripts involved.
---

# Update Documentation Skill

**Operation mode**: Pure agent-based documentation synchronization.

When the user asks to `sync-documentation`, the agent:
1. Scans source code to extract ground truth (public API, provider methods, CLI commands, factory classes)
2. Scans all documentation files
3. Identifies misalignments between code and docs
4. **Auto-fixes documentation** to match code (reports what was changed)

**This is NOT a Python script** - the agent performs all analysis and edits directly.

## Agent-Based Sync Process

When `sync-documentation` is invoked:

### Step 1: Extract Ground Truth from Code

Scan source code to identify:

- **Public API**: Exports from `__all__` in `fake.py` (lines 76-150)
- **Provider methods**: `@provider` decorated methods in `Faker` class (~lines 400-2000)
- **Helper functions**: `create_inner_*` functions (~lines 5400-5700)
- **CLI commands**: Subcommands in `CLI` class (~lines 6500-7000)
- **Factory classes**: `DjangoModelFactory`, `PydanticModelFactory`, `SQLAlchemyModelFactory`, `TortoiseModelFactory`
- **Template classes**: `StringTemplate`, `LazyStringTemplate`

### Step 2: Scan Documentation Files

Read and analyze:

- `README.rst` - Features, installation, quick start
- `CONTRIBUTING.rst` - Developer setup, testing, PR process
- `AGENTS.md` - Agent workflow
- `docs/recipes.rst` - Provider examples (1,859 lines)
- `docs/cheatsheet.rst` - Quick tricks
- `docs/creating_files.rst` - File generation basics, StringTemplate/LazyStringTemplate
- `docs/creating_images.rst` - Image formats
- `docs/creating_pdf.rst` - PDF generation
- `docs/creating_docx.rst` - DOCX generation
- `docs/creating_odt.rst` - ODT generation
- `docs/creating_archives.rst` - ZIP, TAR, EML archives
- `docs/factories.rst` - Factory integrations
- `docs/customisation.rst` - Custom Faker/Factory usage
- `docs/cli.rst` - CLI commands

### Step 3: Identify Misalignments

Compare code ground truth against documentation:

| Doc File | Check Against |
|----------|---------------|
| `README.rst` | Features list vs `__all__` + provider methods |
| `CONTRIBUTING.rst` | Developer prerequisites vs Makefile/pyproject.toml |
| `docs/recipes.rst` | Provider examples vs actual `Faker` methods |
| `docs/cheatsheet.rst` | Tricks vs provider methods |
| `docs/creating_images.rst` | 7 formats (PNG, SVG, BMP, GIF, TIF, PPM, JPG) vs `create_inner_*` |
| `docs/creating_pdf.rst` | PDF methods vs actual implementation |
| `docs/creating_docx.rst` | DOCX methods vs implementation |
| `docs/creating_odt.rst` | ODT methods vs implementation |
| `docs/creating_archives.rst` | ZIP, TAR, EML methods vs implementation |
| `docs/creating_files.rst` | File generation basics, StringTemplate/LazyStringTemplate usage |
| `docs/factories.rst` | Factory classes in `__all__` vs actual implementations |
| `docs/customisation.rst` | Customization APIs vs `Faker`/`Factory` classes |
| `docs/cli.rst` | CLI commands vs `CLI` class subcommands |

Common misalignments:
- Missing provider methods in features list
- Undocumented CLI commands or options
- Missing file format methods
- Broken file path references
- Outdated code examples
- Missing factory integrations

### Step 4: Auto-Fix Documentation

**The agent directly edits documentation files** to align with code:

- Add missing entries to tables
- Update code examples
- Fix file references
- Add missing sections
- Sync provider method names

**SKILL.md is NOT modified** - it remains the source of truth for the skill behavior.

### Step 5: Report Changes

After fixing, report:
- Which files were modified
- What changes were made
- Any issues that couldn't be auto-fixed (ask for clarification if extremely ambiguous)

---

## Documentation Files Overview

| File | Audience | Purpose |
| ---- | -------- | ------- |
| `README.rst` | End users | Features, installation, quick start, API overview |
| `CONTRIBUTING.rst` | Contributors | Developer setup, testing, PR process |
| `AGENTS.md` | AI agents | Mission, architecture, agent workflow |
| `docs/recipes.rst` | Users/developers | Provider examples, usage patterns |
| `docs/cheatsheet.rst` | Users/developers | Quick tricks, scientific content |
| `docs/creating_files.rst` | Users/developers | File generation basics, StringTemplate/LazyStringTemplate |
| `docs/creating_images.rst` | Users/developers | Image format generation (PNG, SVG, BMP, GIF, TIF, PPM, JPG) |
| `docs/creating_pdf.rst` | Users/developers | PDF generation |
| `docs/creating_docx.rst` | Users/developers | DOCX generation |
| `docs/creating_odt.rst` | Users/developers | ODT generation |
| `docs/creating_archives.rst` | Users/developers | ZIP, TAR, EML archives |
| `docs/factories.rst` | Users/developers | Django, Pydantic, SQLAlchemy, TortoiseORM factories |
| `docs/customisation.rst` | Users/developers | Custom Faker/Factory usage |
| `docs/cli.rst` | Users/developers | CLI commands and options |

## When to Update Each File

### README.rst

Update when:
- New provider methods added
- New file formats supported
- Factory integrations added/removed
- CLI commands added/removed
- Installation/requirement changes

Structure to maintain:
- Features list (sync with `__all__` and provider methods)
- Quick start examples
- Installation section
- Supported file formats

### CONTRIBUTING.rst

Update when:
- Developer prerequisites change
- Testing procedure changes
- Code standards change
- Release process changes

Key sections:
- Developer prerequisites (pre-commit, uv, etc.)
- Code standards (ruff, doc8)
- Testing workflow
- Pull request process

### AGENTS.md

Update when:
- Architecture changes
- Agent workflow changes
- Testing rules change

Key sections:
- Project mission (no-dependencies, single-file)
- Architecture table
- Agent workflow
- Testing rules
- Common patterns

### docs/recipes.rst

Update when:
- New provider methods added
- Provider signatures change
- Examples become outdated

Key sections:
- Imports and initialization
- All provider methods with examples

### docs/cheatsheet.rst

Update when:
- New provider methods added
- Quick tricks become outdated

Key sections:
- Scientific content (DOI, ISSN, ORCID, arXiv)
- Quick generation patterns

### docs/creating_files.rst

Update when:
- New file formats added
- StringTemplate/LazyStringTemplate support changes
- Storage backend changes

Key sections:
- BytesValue vs StringValue
- File generation basics
- StringTemplate/LazyStringTemplate usage

### docs/creating_images.rst

Update when:
- New image formats added
- Image generation parameters change
- Supported formats list (PNG, SVG, BMP, GIF, TIF, PPM, JPG)

Key sections:
- Supported formats table
- Image generation examples

### docs/creating_pdf.rst

Update when:
- PDF generation methods change
- Parameters added/removed

Key sections:
- Text PDF vs Graphic PDF
- Page control options

### docs/creating_docx.rst

Update when:
- DOCX generation methods change
- Parameters added/removed

### docs/creating_odt.rst

Update when:
- ODT generation methods change
- Parameters added/removed

### docs/creating_archives.rst

Update when:
- New archive formats added
- Archive generation options change

Key sections:
- ZIP, TAR, EML formats
- Inner file customization

### docs/factories.rst

Update when:
- New factory type added
- Factory decorators change
- Factory parameters change

Key sections:
- Decorators (pre_init, pre_save, post_save, trait)
- Django, Pydantic, SQLAlchemy, TortoiseORM examples

### docs/customisation.rst

Update when:
- Custom Faker/Factory APIs change
- Provider registration changes

### docs/cli.rst

Update when:
- CLI commands added/removed
- CLI options change

---

## Feature-Specific Documentation Checklist

### Adding a New Provider Method

1. **README.rst**: Add to features list
2. **AGENTS.md**: Add code example if relevant
3. **docs/recipes.rst**: Add provider example with `:name:` attribute
4. **docs/cheatsheet.rst**: Add quick trick if applicable
5. **docs/cli.rst**: Add CLI command if exposed

### Adding a New File Format

1. **README.rst**: Add to features list and supported formats
2. **docs/creating_files.rst**: Add basic example
3. **docs/creating_images.rst** or relevant file: Add format-specific section
4. **docs/creating_archives.rst**: If applicable
5. **docs/cli.rst**: Add CLI command

### Adding a New Factory Integration

1. **README.rst**: Add to features list
2. **docs/factories.rst**: Add factory example
3. **docs/customisation.rst**: If applicable

### Adding New CLI Options

1. **docs/cli.rst**: Update command documentation

### Changing Default Values

1. **README.rst**: Update if documented
2. **AGENTS.md**: Update if documented in examples
3. **All relevant docs**: Update code examples

---

## Code Block Naming Convention

AGENTS.md and docs/*.rst use executable code blocks with `:name:` attributes:

**In Markdown (AGENTS.md):**
````markdown
```python name=test_example
from fake import FAKER

FAKER.name()
```
````

**In RST (docs/*.rst):**
```rst
.. code-block:: python
    :name: test_example

    from fake import FAKER

    FAKER.name()
```

When adding examples:
- Use descriptive names: `test_<feature>_<scenario>`
- Use `<!-- continue: <name> -->` in markdown to chain blocks
- Ensure imports are at the top of the first block

---

## Documentation Standards

### RST Formatting

- Line length: 88 characters
- Use `.. code-block:: python` with `:name: test_<name>` for Python
- Use `.. code-block:: sh` for shell commands
- Use `.. note::` for callouts
- Use `.. container:: jsphinx-toggle-emphasis` for collapsible examples

### Code Examples

All code examples in docs/*.rst should be runnable tests. Use the `:name:`
attribute to prefix the block name with `test_`:

```rst
.. code-block:: python
    :name: test_feature_name

    from fake import FAKER

    result = FAKER.name()
```

### Cross-References

- Link to related docs: ``See `docs/recipes.rst`_``
- Reference other sections: ``See `Creating images`_``

---

## Validation Checklist

Before finishing documentation updates:

- [ ] README.rst features match `__all__` and provider methods
- [ ] AGENTS.md code blocks have proper `name=` attributes
- [ ] docs/recipes.rst includes all provider methods
- [ ] docs/creating_images.rst lists all 7 formats (PNG, SVG, BMP, GIF, TIF, PPM, JPG)
- [ ] docs/creating_archives.rst lists all formats (ZIP, TAR, EML)
- [ ] docs/factories.rst documents all factory classes
- [ ] docs/cli.rst CLI commands match `CLI` class
- [ ] CONTRIBUTING.rst prerequisites match Makefile
- [ ] All RST files pass linting
- [ ] Cross-references between docs are valid
- [ ] File paths in docs match actual paths
- [ ] StringTemplate/LazyStringTemplate usage documented in docs/creating_files.rst

---

## What NOT to Document

Do NOT modify documentation that is auto-generated or managed separately.

---

**Use Agent-Based Sync (`sync-documentation`) when:**
- User explicitly asks to "sync documentation"
- You need documentation auto-fixed, not just validated
- You want an interactive, conversational workflow
