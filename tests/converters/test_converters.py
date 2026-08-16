import pytest

from versions.version import Version
from versions.converters.converter import Converter
from versions.converters.registry import ConvertersRegistry

import versions.converters.converter as converter_module

from tests.helpers import HashFormat, SemverFormat


@pytest.fixture()
def converter_registry(monkeypatch) -> ConvertersRegistry:
    """Create isolated converter registry."""
    registry = ConvertersRegistry()

    monkeypatch.setattr(
        converter_module,
        "main_converter_registry",
        registry,
    )

    return registry


def test_new_converter_class_was_registered(converter_registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    assert SemverToHashConverter in converter_registry.get_all()


def test_converter_source_and_target_types():
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    assert SemverToHashConverter.SOURCE_TYPE is SemverFormat
    assert SemverToHashConverter.TARGET_TYPE is HashFormat


def test_converter_can_convert_version():
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    source_version = SemverFormat(version=SemverFormat.EXAMPLE)
    converter = SemverToHashConverter()
    result = converter.convert(source_version)

    assert isinstance(result, HashFormat)
    assert result.version == HashFormat.EXAMPLE


def test_converter_without_source_type_cannot_be_created():
    with pytest.raises(TypeError):
        class InvalidConverter(Converter):
            TARGET_TYPE = HashFormat

            def convert(self, source_version: Version):
                return HashFormat(version=HashFormat.EXAMPLE)


def test_converter_without_target_type_cannot_be_created():
    with pytest.raises(TypeError):
        class InvalidConverter(Converter):
            SOURCE_TYPE = SemverFormat

            def convert(self, source_version: Version):
                return HashFormat(version=HashFormat.EXAMPLE)


def test_converter_source_type_must_be_version_subclass():
    with pytest.raises(TypeError):
        class InvalidConverter(Converter):
            SOURCE_TYPE = str
            TARGET_TYPE = HashFormat

            def convert(self, source_version: Version):
                return HashFormat(version=HashFormat.EXAMPLE)


def test_converter_target_type_must_be_version_subclass():
    with pytest.raises(TypeError):
        class InvalidConverter(Converter):
            SOURCE_TYPE = SemverFormat
            TARGET_TYPE = str

            def convert(self, source_version: Version):
                return "invalid"


def test_source_and_target_types_cannot_be_inherited():
    class ParentConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    with pytest.raises(TypeError):
        class ChildConverter(ParentConverter):
            def convert(self, source_version: Version):
                return HashFormat(version=HashFormat.EXAMPLE)


def test_converter_without_convert_implementation_cannot_be_created():
    with pytest.raises(
        TypeError,
        match=r"AbstractConverter must implement convert\(\) method",
    ):
        class AbstractConverter(Converter):
            SOURCE_TYPE = SemverFormat
            TARGET_TYPE = HashFormat


def test_converter_str():
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    converter = SemverToHashConverter()

    assert str(converter) == (f"SemverToHashConverter: {SemverFormat!r} --> {HashFormat!r}")

def test_abstract_converter_was_not_registered(converter_registry: ConvertersRegistry):
    with pytest.raises(TypeError):
        class AbstractConverter(Converter):
            SOURCE_TYPE = SemverFormat
            TARGET_TYPE = HashFormat
        AbstractConverter not in converter_registry.get_all()


def test_concrete_converter_was_registered(converter_registry: ConvertersRegistry):
    class SemverToHashConverter(Converter):
        SOURCE_TYPE = SemverFormat
        TARGET_TYPE = HashFormat

        def convert(self, source_version: Version):
            return HashFormat(version=HashFormat.EXAMPLE)

    assert SemverToHashConverter in converter_registry.get_all()

@pytest.mark.parametrize(
        "priority", [-10, 0]
)
def test_converter_have_a_positive_priority(priority: int):
    with pytest.raises(ValueError):
        class SemverToHashConverter(Converter):
            SOURCE_TYPE = SemverFormat
            TARGET_TYPE = HashFormat
            PRIORITY = priority
    
            def convert(self, source_version: Version):
                return HashFormat(version=HashFormat.EXAMPLE)

    # assert SemverToHashConverter in converter_registry.get_all()
