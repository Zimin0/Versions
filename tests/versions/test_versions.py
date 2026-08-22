import pytest
from pydantic import ValidationError

from tests.helpers import HashFormat, SemverFormat
from versions.version import Version


@pytest.fixture()
def hash_version() -> HashFormat:
    """Create HashFormat instance."""
    return HashFormat(version=HashFormat.EXAMPLE)


@pytest.fixture()
def semver_version() -> SemverFormat:
    """Create SemverFormat instance."""
    return SemverFormat(version=SemverFormat.EXAMPLE)


def test_regex_and_example_are_immutable(hash_version: HashFormat):
    with pytest.raises(ValidationError):
        hash_version.FORMAT = "123"

    with pytest.raises(AttributeError):
        hash_version.EXAMPLE = "123"

    with pytest.raises(AttributeError):
        HashFormat.EXAMPLE = "123"


def test_can_create_object_only_with_valid_str_version():
    with pytest.raises(ValidationError):
        SemverFormat(version="12345")

    SemverFormat(version=SemverFormat.EXAMPLE)


def test_example_fits_to_regex():
    with pytest.raises(TypeError):
        from versions.version import Version

        class InvalidVersionFormat(Version):
            REGEX = r"\d+\.\d+\.\d?"
            EXAMPLE = "invalid-string"


def test_example_is_empty():
    with pytest.raises(TypeError):
        from versions.version import Version

        class InvalidVersionFormat(Version):
            REGEX = r"\d+\.\d+\.\d?"
            EXAMPLE = ""


def test_invalid_regex():
    with pytest.raises(TypeError):
        from versions.version import Version

        class InvalidVersionFormat(Version):
            REGEX = r"^^^$$$[a-z"
            EXAMPLE = "11.5.7"


def test_new_version_class_was_registered():
    class NewVersion(Version):
        REGEX = r"123"
        EXAMPLE = "123"

    assert NewVersion in Version.formats()


def test_matches_function():
    assert SemverFormat.matches(
        "11.5.7"
    ), "Checking valid version format by Version.matches(). Expecting 'True' result."
    assert not SemverFormat.matches(
        "1234567"
    ), "Checking invalid version format by Version.matches(). Expecting 'False' result."
