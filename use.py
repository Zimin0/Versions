from versions.custom_models import Semver, Hash, BuildVersion
from versions.models import Version, parse_from_str, in_allowed_format

# Any ancentor of Version is immutable.

source = Semver(version="11.5.7+25.3")
target = Hash(version="bh35ag56")

## Use case 1: recognize version's format of provided string.
unknown_version_format = "18.1.5+26.1"
parsed_version = parse_from_str(unknown_version_format)
assert type(parsed_version) == Semver
assert parsed_version.version == "18.1.5+26.1"

## Use case 2: prohibit future execution if Build was provided.
yes = in_allowed_format(BuildVersion.EXAMPLE, Hash|Semver)
print("YES") if yes else print("NO")
# OR by raising a error.
# assert in_allowed_format(BuildVersion.EXAMPLE, Hash|Semver, raise_an_error=True)
# TypeError: Version 'X70-26.2-ahbhge25' is not in allowed formats. Allowed formats: Hash: 'bh35ag56'; Semver: '11.5.7+25.3'; 

# Use case 3: Get all available Version formats
print(Version.formats())

# Можно удалить этот метод?
print(Semver.matches("11.5.7+25.3"))