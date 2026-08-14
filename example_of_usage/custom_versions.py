from versions import Version

class Semver(Version):
    """Internal semantic-like version."""

    REGEX = r"\d+\.\d+\.\d+(?:\+[0-9A-Za-z.-]+)?"
    EXAMPLE = "11.5.7+25.3"


class Hash(Version):
    """Alphanumeric hash containing 8 or 40 characters."""

    REGEX = r"(?:[0-9A-Za-z]{8}|[0-9A-Za-z]{40})"
    EXAMPLE = "bh35ag56"


class ProductionVersion(Version):
    """Production version."""

    REGEX = r"\d+\.\d+-\d+"
    EXAMPLE = "26.2-45"


class BuildVersion(Version):
    """Build version."""

    REGEX = r"XYZ\d+-\d+\.\d+-[0-9A-Za-z]+"
    EXAMPLE = "XYZ70-26.2-ahbhge25"
