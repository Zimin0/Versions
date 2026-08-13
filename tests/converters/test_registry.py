import pytest

from versions.version import Version
from versions.converters.converter import Converter
from versions.converters.errors import ConverterDoesNotImplementedError
from versions.converters.registry import ConvertersRegistry

import versions.converters.converter as converter_module

from tests.helpers import HashFormat, SemverFormat, YearQuartalFormat


@pytest.fixture()
def registry(monkeypatch) -> ConvertersRegistry:
    """Create isolated converter registry."""
    registry = ConvertersRegistry()

    monkeypatch.setattr(
        converter_module,
        "main_converter_registry",
        ConvertersRegistry(),
    )

    return registry


def test_new_registry_is_empty(registry: ConvertersRegistry):
    assert registry.get_all() == ()


def test_can_append_converter(registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    registry.append(SemverToHashConverter)

    assert SemverToHashConverter in registry.get_all()


def test_get_all_returns_all_registered_converters(registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    class HashToSemverConverter(Converter):
        SOURCE_TYPE = HashFormat
        TARGET_TYPE = SemverFormat

        def convert(self, source_version: Version):
            return SemverFormat(version=SemverFormat.EXAMPLE)

    registry.append(SemverToHashConverter)
    registry.append(HashToSemverConverter)

    assert registry.get_all() == (
        SemverToHashConverter,
        HashToSemverConverter,
    )


def test_get_all_returns_tuple(registry: ConvertersRegistry):
    assert isinstance(registry.get_all(), tuple)


def test_can_find_converter(registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    registry.append(SemverToHashConverter)
    found_converter = registry.find_Converter(
        SemverFormat,
        HashFormat,
    )

    assert found_converter is SemverToHashConverter


def test_find_converter_uses_source_and_target_types(registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    class SemverToYearQuartalConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = YearQuartalFormat

        def convert(self, source_version: Version):
            return YearQuartalFormat(
                version=YearQuartalFormat.EXAMPLE,
            )

    registry.append(SemverToHashConverter)
    registry.append(SemverToYearQuartalConverter)

    found_converter = registry.find_Converter(
        SemverFormat,
        YearQuartalFormat,
    )

    assert found_converter is SemverToYearQuartalConverter


def test_converter_direction_matters( registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    registry.append(SemverToHashConverter)

    with pytest.raises(ConverterDoesNotImplementedError):
        registry.find_Converter(
            HashFormat,
            SemverFormat,
        )


def test_find_converter_in_empty_registry_raises_error(registry: ConvertersRegistry):
    with pytest.raises(ConverterDoesNotImplementedError):
        registry.find_Converter(
            SemverFormat,
            HashFormat,
        )


def test_find_not_existing_converter_raises_error(registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    registry.append(SemverToHashConverter)

    with pytest.raises(ConverterDoesNotImplementedError):
        registry.find_Converter(
            HashFormat,
            YearQuartalFormat,
        )


def test_different_registries_are_independent():
    first_registry = ConvertersRegistry()
    second_registry = ConvertersRegistry()

    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    first_registry.append(SemverToHashConverter)

    assert SemverToHashConverter in first_registry.get_all()
    assert SemverToHashConverter not in second_registry.get_all()

