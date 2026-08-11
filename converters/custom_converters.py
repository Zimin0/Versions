from versions.custom_models import Semver, BuildVersion
from versions.models import Version
from versions.converters.base import Convertor

class SemverToBuildConverter(Convertor):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion

    def convert(self, source_version: Version):
        """Convert Semver to BuildVersion."""
        return BuildVersion(version="X70-26.2-ahbhge25")
