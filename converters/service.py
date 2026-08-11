import importlib
from typing import TYPE_CHECKING

from versions.converters.base import main_convertor_registry

if TYPE_CHECKING:
    from versions.models import Version

def load_converters(module: str) -> None:
    """
    Load users' custom converter classes for lib
    
    Use it when custom converters already created and must be registers to be used in convertation.
    """
    importlib.import_module(module)

# could be a private function
def convert_version(source: "Version", target_type: type["Version"]) -> "Version":
    converter_cls = main_convertor_registry.find_convertor(
        in_type=type(source),
        out_type=target_type,
    )
    print(f"Found converter: {converter_cls}")

    converter = converter_cls() # create instance of Converter class.
    return converter.convert(source)
