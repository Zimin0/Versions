from __future__ import annotations
import re
from typing import ClassVar, get_args
from pydantic import BaseModel, ConfigDict, field_validator
from types import UnionType

from versions.errors import VersionValidationError, UnknownVersionFormatError, AmbiguousVersionFormatError

class Version(BaseModel):
    """Base class for version formats."""

    model_config = ConfigDict(
        frozen=True, # makes an instance immutable
        extra="forbid", # no extra fields
    )

    # fild for user
    version: str

    # metadata of concrete class-instance
    REGEX: ClassVar[str]
    EXAMPLE: ClassVar[str]

    # compiles REGEX field
    __pattern: ClassVar[re.Pattern[str]]

    # registry of all available "Version" formats
    __registry: ClassVar[list["Version"]] = []

    def __init_subclass__(cls, **kwargs) -> None:
        """Validate and register every concrete Version subclass."""
        super().__init_subclass__(**kwargs)

        # __dict__ will mnot allow to inherit REGEX or EXAMLE from a parent.
        regex = cls.__dict__.get("REGEX")
        example = cls.__dict__.get("EXAMPLE")

        if not isinstance(regex, str) or not regex.strip():
            raise TypeError(f"{cls.__name__} must define a non-empty REGEX")

        if not isinstance(example, str) or not example.strip():
            raise TypeError(f"{cls.__name__} must define a non-empty EXAMPLE")

        try:
            pattern = re.compile(regex)
        except re.error as exc:
            raise TypeError(f"{cls.__name__}.REGEX is invalid: {exc}") from exc

        # chack EXAMPLE validity
        if pattern.fullmatch(example) is None:
            raise TypeError(f"{cls.__name__}.EXAMPLE={example!r} does not match REGEX={regex!r}")

        cls.__pattern = pattern
        Version.__registry.append(cls)
    
    def __str__(self):
        return f"{type(self).__name__}='{self.version}'"

    @field_validator("version")
    @classmethod
    def validate_version(cls, value: str) -> str:
        if cls is Version:
            raise VersionValidationError("Version is a base class; use a concrete subclass")

        if cls.__pattern.fullmatch(value) is None:
            raise VersionValidationError(
                f"{cls.__name__}: {value!r} does not match {cls.REGEX!r}. Example: {cls.EXAMPLE!r}"
        )

        return value

    @classmethod
    def matches(cls, value: str) -> bool:
        """Return whether the value matches this version format."""
        return (
            cls is not Version
            and cls.__pattern.fullmatch(value) is not None
        )

    @classmethod
    def try_parse(cls, value: str) -> 'Version' | None:
        """Create this version type or return None."""
        if not cls.matches(value):
            return None

        return cls(version=value)

    @classmethod
    def formats(cls) -> tuple[type[Version], ...]:
        """Return all registered concrete version formats."""
        return tuple(Version.__registry)

    # could be a @classmethod?
    def convert_to(self, to: type[Version]) -> Version:
        """Convert version to other format."""
        from versions.converters.service import convert_version

        return convert_version(source=self, target_type=to)

def parse_from_str(value: str) -> Version:
    """
    Parse from string and return Version subclass.
    
    raises: UnknownVersionFormatError, AmbiguousVersionFormatError
    """
    matched_types = [
        version_type
        for version_type in Version.formats()
        if version_type.matches(value)
    ]

    if not matched_types:
        raise UnknownVersionFormatError(f"Unknown version format: {value!r}")

    if len(matched_types) > 1:
        matched_names = ", ".join(
            version_type.__name__
            for version_type in matched_types
        )

        raise AmbiguousVersionFormatError(f"{value!r} matches several formats: {matched_names}")

    version_type = matched_types[0]
    return version_type(version=value)

def in_allowed_format(version: str, formats: UnionType[Version], raise_an_error=False) -> bool:
    """Check that provided `version` is any of allowed `formats`.

    Usage:
    ```python
    yes = in_allowed_format("18.1.5+26.1", Hash|BuildVersion|Semver)
    ```
    """
    v = parse_from_str(version)
    is_valid_format = isinstance(v, formats)
    if not is_valid_format:
        if raise_an_error:
            allowed_formats = "".join(
                f"{f.__name__}: {f.EXAMPLE!r}; "
                for f in get_args(formats)
            )
            raise TypeError(
                f"Version {version!r} is not in allowed formats. "
                f"Allowed formats: "
                f"{allowed_formats}"
            )
    return is_valid_format
    
