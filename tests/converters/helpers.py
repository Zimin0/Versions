import pytest
from versions.converters.registry import ConvertersRegistry
import versions.converters.converter as converter_module

@pytest.fixture()
def registry(monkeypatch) -> ConvertersRegistry:
    """Create isolated converter registry."""
    registry = ConvertersRegistry()

    monkeypatch.setattr(
        converter_module,
        "main_converter_registry",
        registry,
    )

    return registry