from versions.converters.errors import ConverterDoesNotImplementedError, ConverterPriorityConflictError

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

    def __len__(self) -> int:
        return len(self.__all_converters)
    
    def append(self, converter: "Converter"):
        # check that 2 same converters have explicit priority set by user 
        self.__validate_before_append(converter)
        self.__all_converters.append(converter)
    
    def __validate_before_append(self, appended_converter: "Converter"):
        """
        Validate that another converter with the same
        source, target and priority is not already registered.
        """

        for converter in self.__all_converters:
            same_source = (
                converter.SOURCE_TYPE is appended_converter.SOURCE_TYPE
            )
            same_target = (
                converter.TARGET_TYPE is appended_converter.TARGET_TYPE
            )
            same_priority = (
                converter.PRIORITY == appended_converter.PRIORITY
            )

            if same_source and same_target and same_priority:
                raise ConverterPriorityConflictError(
                    "Two converters for the same source and target "
                    "cannot have the same priority. "
                    "Set up different PRIORITIES for these converters. "
                    f"{converter.__name__} and "
                    f"{appended_converter.__name__} both have "
                    f"PRIORITY={appended_converter.PRIORITY}."
                )
            
    def find_converters(self, in_type: "Version", out_type: "Version") -> list["Converter"]:
        """
        Find all fittable Converter subclasses for provided Versions's pair.
        * If exist - return list of appliable Converter subclasses.
        * If does not exist - raise a ConverterDoesNotImplementedError error.
        """
        filtered_converters = []

        if len(self.__all_converters) == 0:
            raise ConverterDoesNotImplementedError("Could not find any converters (none were created). Create a required one: class `Format1ToFormat2Converter(Converter)`: ...")
        
        def source_target_filter_func(elem):
            return in_type == elem.SOURCE_TYPE \
                and out_type == elem.TARGET_TYPE

        sorted_converters_by_priority = sorted(self.__all_converters, key=lambda c: c.PRIORITY)
        filtered_converters = list(filter(source_target_filter_func, sorted_converters_by_priority))

        if len(filtered_converters) != 0:
            return filtered_converters
        
        raise ConverterDoesNotImplementedError(f"Converter for transition {in_type!r} to {out_type!r} does not implemented. To create a converter: class `Format1ToFormat2Converter(Converter)`: ...")

    def get_all(self) -> tuple[type["Version"], ...]:
        """
        Return all registered concrete converters. 
        Objects are not sorted according to their PRIORITY.
        """
        return tuple(self.__all_converters)

# Create a main (singletone) registry
main_converter_registry = ConvertersRegistry()
