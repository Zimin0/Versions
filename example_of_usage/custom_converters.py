from versions.version import Version
from versions.converters.converter import Converter

from example_of_usage.custom_versions import Semver, BuildVersion

class SemverToBuildConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion

    def convert(self, source_version: Version):
        """Convert Semver to BuildVersion."""
        return BuildVersion(version="X70-26.2-ahbhge25")
