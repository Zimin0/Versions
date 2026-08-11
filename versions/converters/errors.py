class VersionConvertationError(Exception):
    """Error during convertation one type of version to other."""

class ConverterDoesNotImplementedError(Exception):
    """Error during a search of applicable Converter for a pair of Version type to convert."""
