class UnknownVersionFormatError(Exception):
    """No registered format matched the supplied version."""


class AmbiguousVersionFormatError(Exception):
    """Several registered formats matched the supplied version."""
