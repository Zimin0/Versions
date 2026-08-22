import pytest

from versions.converters.converter import Converter
from versions.converters.errors import ConverterPriorityConflictError
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


def test_registry_returns_converter_with_highest_priority(registry: ConvertersRegistry):
    class LowPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 10

    class HighPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

    # register the less priority one first
    registry.append(LowPriorityConverter)
    registry.append(HighPriorityConverter)

    result = registry.find_converters(SourceVersion, TargetVersion)

    assert result[0] is HighPriorityConverter
    assert result[1] is LowPriorityConverter


def test_registry_priority_does_not_depend_on_registration_order(
    registry: ConvertersRegistry,
):
    class HighPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

    class LowPriorityConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 100

    registry.append(HighPriorityConverter)
    registry.append(LowPriorityConverter)

    result = registry.find_converters(SourceVersion, TargetVersion)

    assert result[0] is HighPriorityConverter
    assert result[1] is LowPriorityConverter


def test_registry_uses_priority_only_for_matching_converter_pair(
    registry: ConvertersRegistry,
):
    class HighPriorityAnotherTargetConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = AnotherTargetVersion
        PRIORITY = 1

    class MatchingConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 100

    registry.append(HighPriorityAnotherTargetConverter)
    registry.append(MatchingConverter)

    result = registry.find_converters(SourceVersion, TargetVersion)

    assert len(result) == 1
    assert result[0] is MatchingConverter


def test_registry_raise_a_error_when_priorities_are_equal(registry: ConvertersRegistry):
    class FirstConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 5

    class SecondConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 5

    registry.append(FirstConverter)
    with pytest.raises(
        ConverterPriorityConflictError,
        match="Two converters for the same "
        "source and target cannot have the same priority.",
    ):
        registry.append(SecondConverter)


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


def test_chain_of_responsibility_for_converters(registry: ConvertersRegistry):
    class ConverterBroken1(Converter):
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

        def convert(self, source_version: Version):
            raise TypeError("Convertor-1 exception.")

    class ConverterBroken2(Converter):
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 2

        def convert(self, source_version: Version):
            raise TypeError("Convertor-2 exception.")

    class ConverterCorrect3(Converter):
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 3

        def convert(self, source_version: Version):
            print("ConverterCorrect3 was used succesfully.")
            return TargetVersion(version=f"v{source_version.version}234567")

    from versions.converters.service import convert_version

    version = SourceVersion(version="1")
    converted_version = convert_version(
        source=version, target_type=TargetVersion, registry=registry
    )

    assert len(registry) == 3, f"Registered only 3 coverters but found {len(registry)}"
    assert converted_version.version == "v1234567"


def test_registry_rejects_same_source_target_and_priority(registry: ConvertersRegistry):
    class FirstConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

    class SecondConverter:
        SOURCE_TYPE = SourceVersion
        TARGET_TYPE = TargetVersion
        PRIORITY = 1

    registry.append(FirstConverter)

    with pytest.raises(ConverterPriorityConflictError):
        registry.append(SecondConverter)

    assert len(registry) == 1
