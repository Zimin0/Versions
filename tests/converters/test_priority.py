import pytest

from versions.converters.converter import Converter
from versions.converters.registry import ConvertersRegistry
from versions.version import Version


class SourceVersion(Version):
    REGEX = r"\d+"
    EXAMPLE = "1"


class TargetVersion(Version):
    REGEX = r"v\d+"
    EXAMPLE = "v1"


class AnotherTargetVersion(Version):
    REGEX = r"build-\d+"
    EXAMPLE = "build-1"


def test_registry_returns_converter_with_highest_priority():
    class LowPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 10

    class HighPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

    registry = ConvertersRegistry()

    # Специально регистрируем сначала менее приоритетный.
    registry.append(LowPriorityConverter)
    registry.append(HighPriorityConverter)

    result = registry.find_Converter(SourceVersion, TargetVersion)

    assert result is HighPriorityConverter


def test_registry_priority_does_not_depend_on_registration_order():
    class HighPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

    class LowPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 100

    registry = ConvertersRegistry()

    registry.append(HighPriorityConverter)
    registry.append(LowPriorityConverter)

    result = registry.find_Converter(SourceVersion, TargetVersion)

    assert result is HighPriorityConverter


def test_registry_uses_priority_only_for_matching_converter_pair():
    class HighPriorityAnotherTargetConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = AnotherTargetVersion
        PRIORITY = 1

    class MatchingConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 100

    registry = ConvertersRegistry()

    registry.append(HighPriorityAnotherTargetConverter)
    registry.append(MatchingConverter)

    result = registry.find_Converter(SourceVersion, TargetVersion)

    assert result is MatchingConverter


def test_registry_returns_first_registered_converter_when_priorities_are_equal():
    class FirstConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 5

    class SecondConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 5

    registry = ConvertersRegistry()

    registry.append(FirstConverter)
    registry.append(SecondConverter)

    result = registry.find_Converter(SourceVersion, TargetVersion)

    assert result is FirstConverter


def test_converter_rejects_zero_priority():
    with pytest.raises(
        ValueError,
        match=r"must have a positive \(>0\) PRIORITY",
    ):

        class ZeroPriorityConverter(Converter):
            SOURCE_TYPE = SourceVersion
            TARGET_TYPE = TargetVersion
            PRIORITY = 0

            def convert(self, source_version: Version):
                return TargetVersion(version=f"v{source_version.version}")


def test_converter_rejects_negative_priority():
    with pytest.raises(
        ValueError,
        match=r"must have a positive \(>0\) PRIORITY",
    ):

        class NegativePriorityConverter(Converter):
            SOURCE_TYPE = SourceVersion
            TARGET_TYPE = TargetVersion
            PRIORITY = -1

            def convert(self, source_version: Version):
                return TargetVersion(version=f"v{source_version.version}")


def test_converter_default_priority_is_one():
    class DefaultPriorityConverter(Converter):
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion

        def convert(self, source_version: Version):
            return TargetVersion(version=f"v{source_version.version}")

    assert DefaultPriorityConverter.PRIORITY == 1