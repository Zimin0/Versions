# Versions

A small extensible Python library for defining, validating, detecting, and converting version formats.

The library is built around immutable `Version` models. You can define your own version formats with a regular expression and an example, validate version strings, detect their format automatically, restrict allowed formats, and register converters between different version types.

## Features

- Define custom version formats by subclassing `Version`
- Immutable version objects
- Validate version strings against a specific format
- Automatically detect the format of an unknown version string
- Restrict input to a set of allowed formats
- Inspect all registered version formats
- Create custom converters between version formats
- Automatically register converter subclasses
- Load converters from external modules
- Convert one `Version` object to another format

## Requirements

- Python 3.10+
- Pydantic 2

## Installation

After cloning the repository:

```bash
pip install -e .
```

Or install it directly from GitHub:

```bash
pip install "git+https://github.com/<username>/<repository>.git"
```

Replace `<username>` and `<repository>` with the actual GitHub repository path.

## Quick Start (/example_of_usage/main.py)

```python
from versions.version import Version, parse_from_str, in_allowed_format
from versions.converters.registry import main_converter_registry
from versions.converters.service import load_converters

from example_of_usage.custom_versions import (
    Semver,
    Hash,
    BuildVersion,
)

load_converters("example_of_usage.custom_converters")
```

## Defining version objects

Any subclass of `Version` is immutable.

```python
source = Semver(version="11.5.7+25.3")
target = Hash(version="bh35ag56")
```

Once created, a version object cannot be modified.

## Usage

### 1. Detect the format of an unknown version string

Use `parse_from_str()` when you have a string but do not know which registered version format it belongs to.

```python
unknown_version = "18.1.5+26.1"

parsed_version = parse_from_str(unknown_version)

assert type(parsed_version) is Semver
assert parsed_version.version == "18.1.5+26.1"
```

`parse_from_str()` checks registered `Version` subclasses and returns an instance of the matching format.

---

### 2. Restrict input to selected version formats

Use `in_allowed_format()` when only specific formats are acceptable.

```python
allowed = in_allowed_format(
    BuildVersion.EXAMPLE,
    Hash | Semver,
)

print(allowed)
```

In this example, a `BuildVersion` value is checked against the allowed `Hash` and `Semver` formats.

You can also ask the function to raise an error:

```python
in_allowed_format(
    BuildVersion.EXAMPLE,
    Hash | Semver,
    raise_an_error=True,
)
```

Example error:

```text
TypeError: Version 'XYZ70-26.2-ahbhge25' is not in allowed formats.
Allowed formats: Hash: 'bh35ag56'; Semver: '11.5.7+25.3'
```

---

### 3. Inspect all registered version formats

Every `Version` subclass is registered automatically.

```python
print(Version.formats())
```

Example:

```text
(
    <class 'Semver'>,
    <class 'Hash'>,
    <class 'BuildVersion'>,
)
```

This registry is also used internally for automatic format detection.

---

### 4. Validate a string against a specific version format

There are two common ways to validate a version string.

#### Using `matches()`

```python
input_version = "11.5.7+25.3"

if Semver.matches(input_version):
    print("VALID")
else:
    print("INVALID")
```

`matches()` is useful when you only need a boolean result.

#### Creating a version object

```python
from pydantic import ValidationError

input_version = "11.5.7+25.3"

try:
    Semver(version=input_version)
except ValidationError:
    print("INVALID")
else:
    print("VALID")
```

Creating an object is useful when you want both validation and a strongly typed immutable `Version` instance.

---

### 5. Inspect all available converters

Converters are registered automatically when their classes are loaded.

First load a module containing converter implementations:

```python
load_converters("example_of_usage.custom_converters")
```

Then inspect the registry:

```python
print(
    "Available converters:",
    main_converter_registry.get_all(),
)
```

---

### 6. Convert one version format to another

A `Version` object can be converted to another registered version format when a matching converter exists.

```python
source = Semver(version="11.5.7+25.3")

converted = source.convert_to(BuildVersion)

print(converted)
```

The library finds a converter whose source and target types match the requested transition.

## Creating a Custom Version Format

Create a subclass of `Version` and define its `REGEX` and `EXAMPLE`.

```python
from versions.version import Version


class Semver(Version):
    REGEX = r"\d+\.\d+\.\d+(?:\+\d+\.\d+)?"
    EXAMPLE = "11.5.7+25.3"
```

The class is registered automatically and becomes available through:

```python
Version.formats()
```

You can then use it like any other Pydantic model:

```python
version = Semver(version="11.5.7+25.3")
```

And validate strings without creating an object:

```python
Semver.matches("11.5.7+25.3")
```

## Creating a Custom Converter

Create a subclass of `Converter`, define its source and target version types, and implement `convert()`.

```python
from versions.converters.converter import Converter


class SemverToBuildVersionConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion

    def convert(self, source_version: Semver) -> BuildVersion:
        ...
```

Concrete converter subclasses are registered automatically.

After the module containing the converter is loaded, conversion can be performed through:

```python
source.convert_to(BuildVersion)
```

### Converter Priority

Multiple converters may be registered for the same source and target version types.

Use the `PRIORITY` class attribute to control which converter should be selected first.

```python
from versions.converters.converter import Converter


class PreferredSemverToBuildConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 1

    def convert(self, source_version: Semver) -> BuildVersion:
        ...


class FallbackSemverToBuildConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 10

    def convert(self, source_version: Semver) -> BuildVersion:
        ...
```

A **lower `PRIORITY` value means a higher priority**.

In the example above, the converters are evaluated in this order:

```text
PreferredSemverToBuildConverter   PRIORITY = 1
FallbackSemverToBuildConverter    PRIORITY = 10
```

When the library searches for a converter from `Semver` to `BuildVersion`, `PreferredSemverToBuildConverter` is selected first.

The default priority is:

```python
PRIORITY = 1
```

`PRIORITY` must be a positive value greater than zero.

If multiple matching converters have the same priority, their relative order follows their registration order.

The converter registry returned by:

```python
main_converter_registry.get_all()
```

is not sorted by priority. Priority ordering is applied when the library searches for a converter for a specific source/target pair.

## Project Structure

```text
.
├── versions/
│   ├── version.py
│   ├── errors.py
│   └── converters/
│       ├── converter.py
│       ├── registry.py
│       ├── service.py
│       └── errors.py
├── tests/
│   ├── versions/
│   └── converters/
└── example_of_usage/
    ├── custom_versions.py
    ├── custom_converters.py
    └── main.py
```

## Running the Example

From the repository root:

```bash
python -m example_of_usage.main
```

## Project Status

The project is currently under development. The public API may change before the first stable release.

## License

MIT License
