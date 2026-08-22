import pytest

from tests.helpers import HashFormat, SemverFormat, YearQuartalFormat
from versions.converters.converter import Converter
from versions.converters.errors import ConverterDoesNotImplementedError
from versions.converters.registry import ConvertersRegistry
from versions.version import Version


def test_can_append_converter(registry: ConvertersRegistry):
    class SemverToHashConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat
        PRIORITY = 1

    registry.append(SemverToHashConverter)

    assert SemverToHashConverter in registry.get_all()


def test_get_all_returns_all_registered_converters(registry: ConvertersRegistry):
    class SemverToHashConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat
        PRIORITY = 1

    class HashToSemverConverter:
        SOURCE_TYPE = HashFormat
        TARGET_TYPE = SemverFormat
        PRIORITY = 1

    registry.append(SemverToHashConverter)
    registry.append(HashToSemverConverter)

    assert registry.get_all() == (
        SemverToHashConverter,
        HashToSemverConverter,
    )


def test_can_find_converter(registry: ConvertersRegistry):
    class SemverToHashConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat
        PRIORITY = 1

    registry.append(SemverToHashConverter)

    found_converter = registry.find_converters(
        SemverFormat,
        HashFormat,
    )

    assert found_converter[0] is SemverToHashConverter


def test_find_converter_uses_source_and_target_types(
    registry: ConvertersRegistry,
):
    class SemverToHashConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat
        PRIORITY = 1

    class SemverToYearQuartalConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = YearQuartalFormat
        PRIORITY = 1

    registry.append(SemverToHashConverter)
    registry.append(SemverToYearQuartalConverter)

    found_converter = registry.find_converters(
        SemverFormat,
        YearQuartalFormat,
    )

    assert found_converter[0] is SemverToYearQuartalConverter


def test_converter_direction_matters(registry: ConvertersRegistry):
    class SemverToHashConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat
        PRIORITY = 1

    registry.append(SemverToHashConverter)

    with pytest.raises(ConverterDoesNotImplementedError):
        registry.find_converters(
            HashFormat,
            SemverFormat,
        )


def test_find_converter_in_empty_registry_raises_error(
    registry: ConvertersRegistry,
):
    with pytest.raises(ConverterDoesNotImplementedError):
        registry.find_converters(
            SemverFormat,
            HashFormat,
        )


def test_find_not_existing_converter_raises_error(
    registry: ConvertersRegistry,
):
    class SemverToHashConverter:
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat
        PRIORITY = 1

    registry.append(SemverToHashConverter)

    with pytest.raises(ConverterDoesNotImplementedError):
        registry.find_converters(
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
