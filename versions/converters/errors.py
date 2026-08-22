class VersionConvertationError(Exception):
    """Error during convertation one type of version to other."""


class ConverterDoesNotImplementedError(Exception):
    """
    Error during a search of applicable Converter
    for a pair of Version type to convert.
    """


class ConverterPriorityConflictError(Exception):
    "Two converters have the same SOURCE_TYPE, TARGET_TYPE and PRIORITY."


class DoesNotFoundAnyConveter(Exception):
    """Found 0 converters during search."""


class CanNotConvertThisVersion(Exception):
    """Version was not successfully converted."""
