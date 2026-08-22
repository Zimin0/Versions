import pytest

import versions.converters.converter as converter_module
import versions.converters.registry as registry_module

from versions.converters.registry import ConvertersRegistry

@pytest.fixture(autouse=True)
def converter_registry(monkeypatch):
    registry = ConvertersRegistry()

    monkeypatch.setattr(
        converter_module,
        "main_converter_registry",
        registry,
    )

    monkeypatch.setattr(
        registry_module,
        "main_converter_registry",
        registry,
    )

    return registry