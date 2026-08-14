from versions import Version
from versions.converters import Converter

from custom_versions import Semver, BuildVersion

class SemverToBuildConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion

    def convert(self, source_version: Version):
        """Convert Semver to BuildVersion."""
        return BuildVersion(version=BuildVersion.EXAMPLE)
