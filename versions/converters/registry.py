from versions.converters.errors import ConverterDoesNotImplementedError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from  versions.version import Version
    from  versions.converters.converter import Converter

# Todo: make it SingleTone
class ConvertersRegistry():
    """
    A inner registry for all created Converters. 
    A singletone class, do not use it manually.
    """
    __all_Converters: list["Converter"] = []

    def __init__(self):
        self.__all_Converters = []
    
    def append(self, Converter: "Converter"):
        print("Appending new converter:", Converter)
        self.__all_Converters.append(Converter)
        
    def find_Converter(self, in_type: type["Version"], out_type: type["Version"]):
        """
        Find a Converter subclass for provided Versions's pair.
        * If exist - return appliable Converter subclass.
        * If does not exist - raise a ConverterDoesNotImplementedError error.
        """

        if len(self.__all_Converters) == 0:
            raise ConverterDoesNotImplementedError("Could not find any converters (none were created). Create a required one: class `Format1ToFormat2Converter(Converter)`: ...")

        for Converter in self.__all_Converters:
            if in_type == Converter.SOURCE_TYPE \
                and out_type == Converter.TARGET_TYPE:
                    return Converter
        
        raise ConverterDoesNotImplementedError(f"Converter for transition {in_type!r} to {out_type!r} does not implemented. To create a converter: class `Format1ToFormat2Converter(Converter)`: ...")

    def get_all(self) -> tuple[type["Version"], ...]:
        """Return all registered concrete converters."""
        return tuple(self.__all_Converters)

# Create a main (singletone) registry
main_converter_registry = ConvertersRegistry()
