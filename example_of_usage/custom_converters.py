from versions import Version
from versions.converters import Converter

from custom_versions import Semver, BuildVersion

class SemverToBuildConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 1

    def convert(self, source_version: Version):
        """Convert Semver to BuildVersion."""
        return BuildVersion(version=BuildVersion.EXAMPLE)
    
class SemverToBuildConverterByGitlab(Converter):
    """Pairs with SemverToBuildConverter, but has lower PRIORITY. Represents a different way for convertation."""
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 2

    def convert(self, source_version: Version):
        return BuildVersion(version="XYZ70-26.2-secondConvertor")
