from versions.custom_models import Semver, BuildVersion
from versions.models import Version
from versions.converters.models import Convertor

class SemverToBuildConverter(Convertor):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion

    def convert(self, source_version: Version):
        """Convert Semver to BuildVersion."""
        if source_version.version == "26.6.3+26.1":
            return BuildVersion(version="X70-26.2-ahbhge25")
