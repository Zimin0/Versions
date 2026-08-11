# ERRORS
class VersionConvertationError(Exception):
    """Error during convertation one type of version to other."""

class ConvertorDoesNotImplementedError(Exception):
    """Error during a search of applicable Converter for a pair of Version type to convert."""

class NotAConvertorError(Exception):
    """Error showing that object is not a child of Convertor class."""
