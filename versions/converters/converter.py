from abc import ABC, abstractmethod
from typing import ClassVar

from versions.converters.registry import main_converter_registry
from versions.version import Version

class Converter(ABC):
    """Basic abstract class for version convertation."""
    
    SOURCE_TYPE: ClassVar[type[Version]]
    TARGET_TYPE: ClassVar[type[Version]]

    def __init_subclass__(cls, **kwargs):
        """Register every concrete Converter subclass."""
        super().__init_subclass__(**kwargs)

        # __dict__ will mnot allow to inherit REGEX or EXAMLE from a parent
        source_type = cls.__dict__.get("SOURCE_TYPE")
        target_type = cls.__dict__.get("TARGET_TYPE")

        if not issubclass(source_type, Version) or not source_type:
            raise TypeError(f"{cls.__name__} must define a non-empty SOURCE_TYPE")

        if not issubclass(target_type, Version) or not target_type:
            raise TypeError(f"{cls.__name__} must define a non-empty TARGET_TYPE")

        main_converter_registry.append(cls)
    
    def __str__(self):
        return f"{self.__name__}: {self.SOURCE_TYPE!r} --> {self.TARGET_TYPE!r}"

    @abstractmethod
    def convert(self, source_version: Version):
        ...

