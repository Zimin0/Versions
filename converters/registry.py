from versions.converters.errors import ConvertorDoesNotImplementedError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from versions.models import Version
    from versions.converters.base import Convertor

# Todo: make it SingleTone
class ConvertorsRegistry():
    """
    A inner registry for all created Convertors. 
    A singletone class, do not use it manually.
    """
    __all_convertors: list["Convertor"] = []

    def __init__(self):
        self.__all_convertors = []
    
    def append(self, convertor: "Convertor"):
        print("Appending new converter:", convertor)
        self.__all_convertors.append(convertor)
        
    def find_convertor(self, in_type: type["Version"], out_type: type["Version"]):
        """
        Find a Convertor subclass for provided Versions's pair.
        * If exist - return appliable Convertor subclass.
        * If does not exist - raise a ConvertorDoesNotImplementedError error.
        """

        if len(self.__all_convertors) == 0:
            raise ConvertorDoesNotImplementedError("Could not find any converters (none were created). Create a required one: class `Format1ToFormat2Converter(Convertor)`: ...")

        for convertor in self.__all_convertors:
            if in_type == convertor.SOURCE_TYPE \
                and out_type == convertor.TARGET_TYPE:
                    return convertor
        
        raise ConvertorDoesNotImplementedError(f"Converter for transition {in_type!r} to {out_type!r} does not implemented. To create a converter: class `Format1ToFormat2Converter(Convertor)`: ...")

    def get_all(self) -> tuple[type["Version"], ...]:
        """Return all registered concrete converters."""
        return tuple(self.__all_convertors)

# Create a main (singletone) registry
main_convertor_registry = ConvertorsRegistry()
