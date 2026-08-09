from abc import ABC, abstractmethod
from typing import ClassVar
from pydantic import BaseModel, ConfigDict

from versions.models import Version

class Convertor(BaseModel, ABC):
    """Basic abstract class for version convertation."""

    model_config = ConfigDict(
        frozen=True, # makes an instance immutable
        extra="forbid", # no extra fields
    )
    
    SOURCE_TYPE: ClassVar[Version]
    TARGET_TYPE: ClassVar[Version]

    # All available convertors
    __registry: ClassVar[list["Convertor"]] = []

    def __init_subclass__(cls, **kwargs):
        """Register every concrete Convertor subclass."""
        super().__init_subclass__(**kwargs)

        # __dict__ will mnot allow to inherit REGEX or EXAMLE from a parent.
        source_type = cls.__dict__.get("SOURCE_TYPE")
        target_type = cls.__dict__.get("TARGET_TYPE")

        if not issubclass(source_type, Version) or not source_type:
            raise TypeError(f"{cls.__name__} must define a non-empty SOURCE_TYPE")

        if not issubclass(target_type, Version) or not target_type:
            raise TypeError(f"{cls.__name__} must define a non-empty TARGET_TYPE")

        Convertor.__registry.append(cls)

    @classmethod
    def formats(cls) -> tuple[type[Version], ...]:
        """Return all registered concrete converters."""
        return tuple(Convertor.__registry)

    @abstractmethod
    def convert(self, source_version: Version):
        ...

