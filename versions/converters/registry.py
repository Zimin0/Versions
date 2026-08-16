from versions.converters.errors import ConverterDoesNotImplementedError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from versions.version import Version
    from versions.converters.converter import Converter

# Todo: make it SingleTone
class ConvertersRegistry():
    """
    A inner registry for all created Converters. 
    A singletone class, do not use it manually.
    """
    __all_converters: list["Converter"] = []

    def __init__(self):
        self.__all_converters = []
    
    def append(self, Converter: "Converter"):
        self.__all_converters.append(Converter)
        
    def find_Converter(self, in_type: type["Version"], out_type: type["Version"]):
        """
        Find a Converter subclass for provided Versions's pair.
        * If exist - return appliable Converter subclass.
        * If does not exist - raise a ConverterDoesNotImplementedError error.
        """

        if len(self.__all_converters) == 0:
            raise ConverterDoesNotImplementedError("Could not find any converters (none were created). Create a required one: class `Format1ToFormat2Converter(Converter)`: ...")

        sorted_converters_by_priority = sorted(self.__all_converters, key=lambda c: c.PRIORITY)
        for Converter in sorted_converters_by_priority:
            if in_type == Converter.SOURCE_TYPE \
                and out_type == Converter.TARGET_TYPE:
                    return Converter
        
        raise ConverterDoesNotImplementedError(f"Converter for transition {in_type!r} to {out_type!r} does not implemented. To create a converter: class `Format1ToFormat2Converter(Converter)`: ...")

    def get_all(self) -> tuple[type["Version"], ...]:
        """
        Return all registered concrete converters. 
        Objects are not sorted according to their PRIORITY.
        """
        return tuple(self.__all_converters)

# Create a main (singletone) registry
main_converter_registry = ConvertersRegistry()
