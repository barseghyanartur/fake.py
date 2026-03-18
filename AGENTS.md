# AGENTS.md — fake.py

**Repository**: https://github.com/barseghyanartur/fake.py
**Maintainer**: Artur Barseghyan <artur.barseghyan@gmail.com>

This file is for AI agents and developers using AI assistants to work on or with
fake.py. It covers two distinct roles: **using** the package in application code,
and **developing/extending** the package itself.

---

## 1. Project Mission (Never Deviate)

> Minimalistic, standalone fake data generator with no dependencies.

- Generates fake data for testing and development
- Zero runtime dependencies (only optional dependencies for testing, development, documentation and building)
- Single-file architecture with self-contained providers
- Random texts, (person) names, emails, URLs, dates, IPs, and primitive Python data types
- GEO data (city, country, geo-location, country code, latitude, longitude, locales)
- IBANs and ISBNs
- File formats (PDF, DOCX, ODT, RTF, EPUB, TXT, PNG, SVG, BMP, GIF, TIF, PPM, JPG, WAV, ZIP, TAR, EML)
- StringTemplate and LazyStringTemplate for dynamic content generation
- FILE_REGISTRY for tracking and cleanup of generated files
- CLI for generating data from command line
- Factories (dynamic fixtures) for Django, Pydantic, TortoiseORM, and SQLAlchemy

---

## 2. Using fake.py in Application Code

### Simple case

```python name=test_simple_usage
from fake import FAKER

name = FAKER.name()
email = FAKER.email()
text = FAKER.text()

assert name  # "John Doe"
assert email  # "john@example.com"
assert text  # Paragraph of lorem ipsum
```

### File generation

```python name=test_file_generation
from fake import FAKER, FILE_REGISTRY

txt_file = FAKER.txt_file()
docx_file = FAKER.docx_file(nb_pages=2)
pdf_file = FAKER.pdf_file(nb_pages=5)
zip_archive = FAKER.zip_file(options={"count": 10})

assert txt_file
assert docx_file
assert pdf_file
assert zip_archive

FILE_REGISTRY.clean_up()  # Remove generated files
```

### StringTemplate for static content

```python name=test_string_template_static
from fake import FAKER, StringTemplate

template = StringTemplate("""
    Date: {date}
    To: {name}
    Subject: {sentence(nb_words=8)}
""")
result = str(template)
assert result
assert "Date:" in result
assert "To:" in result
```

### LazyStringTemplate for dynamic content

```python name=test_lazy_string_template_dynamic
from fake import FAKER, LazyStringTemplate

template = LazyStringTemplate("Hello {name}!")

for i in range(3):
    result = str(template)
    assert result.startswith("Hello ")
    assert result.endswith("!")
```

### Archive with custom inner files

```python name=test_archive_with_custom_inner_files
from fake import FAKER, FILE_REGISTRY, LazyStringTemplate, create_inner_generic_file

xml_template = LazyStringTemplate("""
    <?xml version="1.0"?>
    <article>
        <title>{sentence(nb_words=8)}</title>
        <body>{paragraph(nb_sentences=5)}</body>
    </article>
""")

archive = FAKER.zip_file(
    options={
        "count": 3,
        "create_inner_file_func": create_inner_generic_file,
        "create_inner_file_args": {
            "content": xml_template,
            "extension": "xml",
            "dir_path": "{dir_path(depth=2)}",
        },
    }
)
assert archive
FILE_REGISTRY.clean_up()
```

---

## 3. Architecture

### Single-File Structure

The entire package lives in `fake.py` (~10,000 lines). Key sections:

| Section | Lines | Purpose |
| ------- | ----- | ------- |
| **Imports & Config** | 1-200 | All imports, `__all__`, constants |
| **Core Classes** | 400-700 | `StringValue`, `BytesValue`, `StringTemplate`, `LazyStringTemplate`, storage classes |
| **Provider Methods** | 2000-8000 | All `FAKER.` methods organized by category |
| **Helper Functions** | 5400-5700 | `create_inner_*` functions for archives |
| **Tests** | 7000-10400 | `TestFaker`, `TestCLI`, `TestStringTemplate` classes |

### Key Classes

| Class | Purpose |
| ----- | ------- |
| `Faker` | Main class with all provider methods |
| `FAKER` | Default singleton instance |
| `StringTemplate` | Renders at construction time (subclasses `str`) |
| `LazyStringTemplate` | Renders on every `str()` call |
| `StringValue` | File path wrapper with `.data` dict |
| `BytesValue` | Raw bytes wrapper with `.data` dict |
| `FileSystemStorage` | Default storage backend |
| `FILE_REGISTRY` | Tracks generated files for cleanup |

### Resolution Pipeline

For StringTemplate/LazyStringTemplate resolution in `generic_file`:

1. Check if content is `StringTemplate` or `LazyStringTemplate` instance
2. Call `str(content)` to render (triggers fresh render for LazyStringTemplate)
3. Proceed with normal string write path

### Key Files

| File | Purpose |
| ---- | ------- |
| `fake.py` | Entire package (single file) |
| `pyproject.toml` | Build, ruff, pytest configuration |
| `Makefile` | Development commands |
| `conftest.py` | pytest fixtures |

---

## 4. Coding Conventions

### Formatting

- Line length: **80 characters** (ruff).
- Import sorting: `ruff`.
- Target: Python 3.9+. Run `make ruff` to check.

Run all linting checks:

```sh
make pre-commit
```

### Ruff rules in effect

`B`, `C4`, `E`, `F`, `G`, `I`, `ISC`, `INP`, `N`, `PERF`, `Q`, `SIM`.

Explicitly ignored (check pyproject.toml for current settings).

### Style

- Every module should have `__author__`, `__copyright__`, `__license__` at module level.
- Always chain exceptions: `raise X(...) from exc`.
- Type annotations on all public functions.
- Use `@provider(tags=(...))` decorator for Faker methods.
- Follow existing docstring format (Sphinx-style with `:param`:).

### Pull requests

Target the `dev` branch only. Never open a PR directly to `main`.

---

## 5. Agent Workflow: Adding Features or Fixing Bugs

When asked to add a feature or fix a bug, follow these steps in order:

1. **Check the mission** — Does the change preserve the no-dependencies policy and single-file architecture?
2. **Identify the correct location** — Find the method in `fake.py`:
   - Provider methods are in the `Faker` class (~lines 2000-8000)
   - Helper functions (`create_inner_*`) are standalone functions (~lines 5400-5700)
3. **For bug fixes: write the regression test first** — Add a test that reproduces the bug in the `TestFaker` class
4. **Implement the change** in the correct location
5. **Export** new public symbols from `__all__` tuple (line ~75)
6. **Write tests** - Add test cases for new functionality in `TestFaker` class
7. **Update `README.rst`** if the API changed
8. **Suggest running:** `make test`
9. **Suggest running:** `make pre-commit`

### Adding a new provider method

```python name=test_adding_new_provider_method
from fake import provider

@provider(tags=("MyCategory",))
def my_method(self, param: str = "default") -> str:
    """My method description.

    :param param: Description.
    :return: Description.
    :rtype: str
    """
    return f"result: {param}"
```

### Adding a new create_inner_* function

<!-- pytestfixture: Optional -->
```python name=test_adding_new_create_inner_functions
from fake import BaseStorage, FAKER, StringValue

def create_inner_my_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    **kwargs,
) -> StringValue:
    """Create inner MY file."""
    return FAKER.my_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        **kwargs,
    )
```

### Adding StringTemplate/LazyStringTemplate support

When adding support for templates in a new method:

1. Accept `Union[bytes, str, StringTemplate, LazyStringTemplate]` as content parameter
2. Before processing, check: `if isinstance(content, (StringTemplate, LazyStringTemplate)): content = str(content)`
3. Document the behavior in docstring

### Acceptable new features

- Additional file format support
- New provider methods
- StringTemplate/LazyStringTemplate integration
- Storage backend improvements

### Forbidden

- Adding external dependencies
- Breaking existing provider signatures
- Moving code out of fake.py (single-file architecture)

---

## 6. Testing Rules

### Running tests

```sh
make test                   # Run all tests
```

Or use unittest directly:

```sh
.venv/bin/python -m unittest fake.TestFaker.test_method_name
```

### Test layout

Tests are embedded in `fake.py` at the end of the file:

```text
fake.py:
    TestCLI class           — CLI tests (line ~6900)
    TestFaker class         — Main provider tests (line ~7169)
    TestStringTemplate      — Template tests (line ~7900)
    TestLazyStringTemplate  — Lazy template tests
```

### Test style

- **Use unittest style only** — Although pytest is used as the test runner,
  no third-party test imports are allowed due to the no-dependency, portable
  nature of the package. Use `unittest.TestCase` classes, `self.assert*`
  methods, and `self.subTest()` for parameterized assertions.
- **No pytest fixtures or plugins** — Package tests must work without
  `pytest`-specific features so they can run with any unittest-compatible
  runner.
  Note that documentation is tested separately using `pytest` and
  `pytest-codeblock`; all documentation fixtures are defined in root
  `conftest.py`.
- **Documentation tests use pytest-style** — Code examples in `.rst` and `.md`
  files (tested via `pytest-codeblock`) run outside unittest context. Use
  plain `assert` statements instead of `self.assert*` methods.

- Use `setUp` to initialize `self.faker = FAKER`.
- Use `tearDown` to call `FILE_REGISTRY.clean_up()`.
- Use `self.subTest()` for multiple assertions in one test.
- Use `os.path.exists()` to verify file generation.
- **Always use `self.faker`** instead of `FAKER` directly — this ensures tests
  work with `__copy_fake.py` which tests the module in isolation.
- **Don't use inline imports** for module-level symbols like `StringTemplate`,
  `LazyStringTemplate`, `Path`, `BytesIO`, `zipfile`, `tarfile` — they are
  already imported at the top of the file.
- **Use standard library imports directly** — `import zipfile`
  not `import zipfile as _zf`.

### Test example

```python name=test_test_example
def test_my_method(self) -> None:
    with self.subTest("Basic case"):
        result = self.faker.my_method()
        self.assertTrue(result)

    with self.subTest("With parameter"):
        result = self.faker.my_method(param="value")
        self.assertEqual(result, "result: value")
```

### Archive test example

When testing zip/tar archives, use `BytesIO(bytes(raw))` and access the
archive through the standard library:

```python name=test_archive_test_example
def test_zip_dir_path_literal(self):
    """dir_path as a literal string places the file at that subpath."""
    raw = self.faker.zip(
        options={
            "count": 1,
            "create_inner_file_func": create_inner_txt_file,
            "create_inner_file_args": {
                "dir_path": "level1/level2/level3",
            },
            "directory": "",
        }
    )

    with zipfile.ZipFile(BytesIO(bytes(raw)), "r") as zf:
        names = zf.namelist()

    assert len(names) == 1
    parts = Path(names[0]).parts
    assert parts[0] == "level1"
    assert parts[1] == "level2"
    assert parts[2] == "level3"

def test_tar_dir_path_literal(self):
    """Same guarantee holds for tar()."""
    raw = self.faker.tar(
        options={
            "count": 1,
            "create_inner_file_func": create_inner_txt_file,
            "create_inner_file_args": {
                "dir_path": "a/b/c",
            },
            "directory": "",
        }
    )

    with tarfile.open(fileobj=BytesIO(bytes(raw))) as tf:
        names = tf.getnames()

    assert len(names) == 1
    parts = Path(names[0]).parts
    assert parts[:3] == ("a", "b", "c")
```

---

## 7. Prompt Templates

**Explaining usage to a user:**
> You are an expert in fake data generation. Explain how to use fake.py to
> generate [type of data]. Show how to use StringTemplate vs LazyStringTemplate
> and when each is appropriate.

**Implementing a new feature:**
> Extend fake.py with [new provider/format]. Follow the AGENTS.md agent workflow:
> identify the correct location, implement, add tests, update README.
> Preserve the no-dependencies policy and single-file architecture.

**Fixing a bug:**
> Reproduce [bug] with a new test case. The test must fail before your fix.
> Then fix the issue, add tests for both failure and success cases.

**Reviewing a change:**
> Review this fake.py change against AGENTS.md: Does it preserve no-dependencies
> policy? Does it follow the single-file architecture? Are new features tested?
> Does it update `__all__` correctly?

---

## 8. Common Patterns

### File generation with storage

```python name=test_file_generation_with_storage
from fake import FAKER, FileSystemStorage, FILE_REGISTRY

storage = FileSystemStorage(root_path="/tmp/myapp", rel_path="exports")
file = FAKER.pdf_file(storage=storage, prefix="report_")
assert file
FILE_REGISTRY.clean_up()
```

### Batch generation in archive

```python name=test_batch_generation_in_archive
from fake import FAKER, FILE_REGISTRY, create_inner_txt_file

archive = FAKER.zip_file(
    options={
        "count": 5,
        "create_inner_file_func": create_inner_txt_file,
        "create_inner_file_args": {"prefix": "file_"},
        "directory": "docs",
    }
)
assert archive
FILE_REGISTRY.clean_up()
```

### Custom content with template

```python name=test_custom_content_with_template
from fake import FAKER, LazyStringTemplate, FILE_REGISTRY

template = LazyStringTemplate("{name} lives in {city}")
files = [FAKER.txt_file(text=str(template)) for _ in range(3)]
for file in files:
    assert file
FILE_REGISTRY.clean_up()
```
