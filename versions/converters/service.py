import importlib
from typing import TYPE_CHECKING

from versions.converters.errors import CanNotConvertThisVersion, DoesNotFoundAnyConveter
from versions.converters.registry import main_converter_registry, ConvertersRegistry

if TYPE_CHECKING:
    from versions.version import Version

def load_converters(module: str) -> None:
    """
    Load users' custom converter classes for lib
    
    Use it when custom converters already created and must be registers to be used in convertation.
    """
    importlib.import_module(module)

# could be a private function
def convert_version(
        source: "Version", 
        target_type: type["Version"], 
        registry: ConvertersRegistry = main_converter_registry
        ) -> "Version":
    
    converter_cls_list = registry.find_converters(
        in_type=type(source),
        out_type=target_type,
    )

    if not converter_cls_list:
        raise DoesNotFoundAnyConveter("Found 0 converters during search.")

    converted_version = None

    for conv_cls in converter_cls_list:
        converter = conv_cls() # create instance of Converter class.
        try: 
            converted_version = converter.convert(source)
            return converted_version
        except Exception as error: # TODO: should be a specific exception?
            # print(error)
            continue # TODO: add logging of an error 
        
    if converted_version is None:
        raise CanNotConvertThisVersion(
            f"Can not convert version {source!r} to {target_type.__name__!r}. " \
            f"Converters were tried: {len(converter_cls_list)}")

    return converted_version
