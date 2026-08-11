from versions.version import Version

class HashFormat(Version):
    REGEX = r"(?:[0-9A-Za-z]{8}|[0-9A-Za-z]{40})"
    EXAMPLE = "bh35ag56"


class YearQuartalFormat(Version):
    REGEX = r"\d+\.\d+-\d+"
    EXAMPLE = "26.2-45"


class SemverFormat(Version):
    REGEX = r"\d+\.\d+\.\d?"
    EXAMPLE = "11.5.7"
