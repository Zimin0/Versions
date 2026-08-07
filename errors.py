class VersionValidationError(ValueError):
    """Base error for invalid version values."""


class UnknownVersionFormatError(VersionValidationError):
    """No registered format matched the supplied version."""


class AmbiguousVersionFormatError(VersionValidationError):
    """Several registered formats matched the supplied version."""
