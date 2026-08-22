from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import PositiveInt

from versions.converters.registry import main_converter_registry
from versions.version import Version


class Converter(ABC):
    """Basic abstract class for version convertation."""

    SOURCE_TYPE: ClassVar[type[Version]]
    TARGET_TYPE: ClassVar[type[Version]]
    PRIORITY: ClassVar[PositiveInt] = 1

    def __init_subclass__(cls, **kwargs):
        """Register every concrete Converter subclass."""
        super().__init_subclass__(**kwargs)

        # __dict__ will mnot allow to inherit REGEX or EXAMLE from a parent
        source_type = cls.__dict__.get("SOURCE_TYPE")
        target_type = cls.__dict__.get("TARGET_TYPE")
        priority = cls.PRIORITY  # PROIROTY can be inherited
        convert_method = cls.__dict__.get("convert")  # method convert must be defined

        if convert_method is None:
            raise TypeError(f"{cls.__name__} must implement convert() method")

        if not source_type or not issubclass(source_type, Version):
            raise TypeError(f"{cls.__name__} must define a non-empty SOURCE_TYPE")

        if not target_type or not issubclass(target_type, Version):
            raise TypeError(f"{cls.__name__} must define a non-empty TARGET_TYPE")

        if priority <= 0:
            raise ValueError(f"{cls.__name__} must have a positive (>0) PRIORITY")

        main_converter_registry.append(cls)

    def __str__(self):
        return (
            f"{self.__class__.__name__}: {self.SOURCE_TYPE!r} --> {self.TARGET_TYPE!r}"
        )

    @abstractmethod
    def convert(self, source_version: Version): ...
