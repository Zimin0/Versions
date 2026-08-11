import importlib
from typing import TYPE_CHECKING

from versions.converters.converter import main_converter_registry

if TYPE_CHECKING:
    from versions.version import Version

def load_converters(module: str) -> None:
    """
    Load users' custom converter classes for lib
    
    Use it when custom converters already created and must be registers to be used in convertation.
    """
    importlib.import_module(module)

# could be a private function
def convert_version(source: "Version", target_type: type["Version"]) -> "Version":
    converter_cls = main_converter_registry.find_Converter(
        in_type=type(source),
        out_type=target_type,
    )

    converter = converter_cls() # create instance of Converter class.
    return converter.convert(source)
