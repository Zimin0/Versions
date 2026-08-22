from custom_versions import BuildVersion, Semver

from versions import Version
from versions.converters import Converter
from versions.converters.errors import CanNotConvertThisVersion


class BrokenSemverToBuildConverter(Converter):
    """
    This convertor is broken.
    Library will try to convert version
    by this convertor first due to its highest priority.
    Will catch a error and go to second priority converter - SemverToBuildConverter.
    """

    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 1

    def convert(self, source_version: Version):
        """Brokent convert Semver to BuildVersion."""
        raise CanNotConvertThisVersion("    I'am broken converter. Skip me...")


class SemverToBuildConverter(Converter):
    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 2

    def convert(self, source_version: Version):
        """Convert Semver to BuildVersion."""
        return BuildVersion(version=BuildVersion.EXAMPLE)


class SemverToBuildConverterByGitlab(Converter):
    """
    Pairs with SemverToBuildConverter, but has lower PRIORITY.
    Represents a different way for convertation.
    """

    SOURCE_TYPE = Semver
    TARGET_TYPE = BuildVersion
    PRIORITY = 3

    def convert(self, source_version: Version):
        return BuildVersion(version="XYZ70-26.2-secondConvertor")
